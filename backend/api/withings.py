import os
import time
import json
import threading
import requests
import webbrowser
from pathlib import Path
from datetime import datetime
from urllib.parse import urlencode, parse_qs, urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from backend.common.database import save_withings_data, save_api_token, get_api_token
from backend.common.logging_config import logger

CREDS_FILE = Path("backend/user_data/withings_creds.json")
TOKEN_FILE = Path("backend/user_data/withings_token.json")
TOKEN_URL = "https://wbsapi.withings.net/v2/oauth2"
API_ENDPOINT = "https://wbsapi.withings.net/measure"
AUTHORIZE_URL = "https://account.withings.com/oauth2_user/authorize2"

def load_credentials():
    try:
        if CREDS_FILE.exists():
            with open(CREDS_FILE, "r") as f:
                c = json.load(f)
            return c.get("client_id"), c.get("client_secret"), c.get("callback_uri")
    except Exception as e:
        logger.error(f"cred error: {e}")
    return os.getenv("WITHINGS_CLIENT_ID"), os.getenv("WITHINGS_CLIENT_SECRET"), "http://localhost:8000/callback"

CLIENT_ID, CLIENT_SECRET, REDIRECT_URI = load_credentials()

auth_code = None

def handle_callback(port=8000):
    def handler(self, *args):
        global auth_code
        q = parse_qs(urlparse(self.path).query)
        if "code" in q:
            auth_code = q["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Auth OK. You can close this window.")
            threading.Thread(target=self.server.shutdown).start()
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Auth failed.")
    HTTPServer(("localhost", port), type("H", (BaseHTTPRequestHandler,), {"do_GET": handler})).serve_forever()

def save_token(t):
    t["created"] = int(time.time())
    TOKEN_FILE.parent.mkdir(exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        json.dump(t, f)
    exp = datetime.utcfromtimestamp(t["created"] + t.get("expires_in", 3600)).isoformat()
    save_api_token("withings", t, exp)

def refresh_token(rf):
    d = {
        "action": "requesttoken",
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": rf,
    }
    resp = requests.post(TOKEN_URL, data=d)
    if resp.status_code == 200:
        j = resp.json()
        if j.get("status") == 0 and "body" in j:
            b = j["body"]
            t = {
                "access_token": b["access_token"],
                "refresh_token": b["refresh_token"],
                "expires_in": b.get("expires_in", 3600),
            }
            save_token(t)
            return t
    return None

def start_auth():
    global auth_code
    auth_code = None
    threading.Thread(target=handle_callback, daemon=True).start()
    time.sleep(1)
    p = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "user.metrics",
        "state": "daylog_auth",
    }
    webbrowser.open(f"{AUTHORIZE_URL}?{urlencode(p)}")
    s = time.time()
    while auth_code is None and time.time() - s < 300:
        time.sleep(1)
    if auth_code is None:
        return None
    d = {
        "action": "requesttoken",
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }
    resp = requests.post(TOKEN_URL, data=d)
    if resp.status_code == 200:
        j = resp.json()
        if j.get("status") == 0 and "body" in j:
            b = j["body"]
            t = {
                "access_token": b["access_token"],
                "refresh_token": b["refresh_token"],
                "expires_in": b.get("expires_in", 3600),
            }
            save_token(t)
            return t
    return None

def load_token():
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "r") as f:
            t = json.load(f)
        if time.time() < t.get("created", 0) + t.get("expires_in", 3600) - 300:
            return t
        if "refresh_token" in t:
            r = refresh_token(t["refresh_token"])
            if r:
                return r
    return start_auth()

def get_withings():
    logger.info("Withings: fetching weight data")
    if not CLIENT_ID or not CLIENT_SECRET:
        logger.warning("Withings credentials missing")
        return {"status": "not_configured"}
    tok = load_token()
    if not tok or "access_token" not in tok:
        logger.error("Withings token unavailable")
        return None
    r = requests.get(
        f"{API_ENDPOINT}?action=getmeas&meastype=1",
        headers={"Authorization": f"Bearer {tok['access_token']}"},
    )
    if r.status_code == 200:
        j = r.json()
        if j.get("status") == 0 and j.get("body", {}).get("measuregrps"):
            v = j["body"]["measuregrps"][0]["measures"][0]["value"]
            kg = v / 1000
            logger.info(f"Withings latest weight: {kg:.1f} kg")
            save_withings_data(kg)
            return {"weight": kg}
        logger.error("Withings: no weight data")
    else:
        logger.error(f"Withings request failed: {r.text}")
    return None
