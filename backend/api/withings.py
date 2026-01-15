from auth.azure_auth import azure_auth, set_secret, get_secret
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from datetime import date, datetime, timedelta
import os
import time
import requests
import uvicorn
import logging
from database.database import init_db, insert_data_withings

logging.basicConfig(level=logging.WARNING)
log = logging.getLogger("withings")
log.setLevel(logging.INFO)

START_DATE = date(2024, 6, 1)

AUTHORIZE_URL = "https://account.withings.com/oauth2_user/authorize2"
TOKEN_URL = "https://wbsapi.withings.net/v2/oauth2"
GET_MEASUREMENTS_URL = "https://wbsapi.withings.net/measure?action=getmeas"

app = FastAPI()

WITHINGS_CLIENT_ID_SECRET = os.environ.get("WITHINGS_CLIENT_ID_SECRET", "withings-client-id")
WITHINGS_CLIENT_SECRET_SECRET = os.environ.get("WITHINGS_CLIENT_SECRET_SECRET", "withings-client-secret")
WITHINGS_ACCESS_TOKEN_SECRET = os.environ.get("WITHINGS_ACCESS_TOKEN_SECRET", "daylog-withings-access-token")
WITHINGS_REFRESH_TOKEN_SECRET = os.environ.get("WITHINGS_REFRESH_TOKEN_SECRET", "daylog-withings-refresh-token")
WITHINGS_USERID_SECRET = os.environ.get("WITHINGS_USERID_SECRET", "daylog-withings-userid")

def get_client_creds():
    log.info(
        "Fetching Withings client credentials (id_secret=%s, secret_secret=%s)",
        WITHINGS_CLIENT_ID_SECRET,
        WITHINGS_CLIENT_SECRET_SECRET,
    )
    withings_client_id, withings_client_secret = azure_auth(
        WITHINGS_CLIENT_ID_SECRET,
        WITHINGS_CLIENT_SECRET_SECRET,
    )
    return withings_client_id, withings_client_secret

@app.get("/")
def root():
    client_id, _ = get_client_creds()
    url = f"{AUTHORIZE_URL}?response_type=code&client_id={client_id}&state=OK&scope=user.metrics&redirect_uri=http://localhost:8081/callback"
    return RedirectResponse(url=url)

@app.get("/callback")
def callback(code: str):
    return get_access_token(code)

def get_access_token(code: str):
    log.info(f"Code received: {code}")
    client_id, client_secret = get_client_creds()
    params = {
        "action": "requesttoken",
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": "http://localhost:8081/callback"
    }
    req = requests.post(TOKEN_URL, params)
    resp = req.json()
    log.info(f"Token response: {resp}")
    
    if resp.get("status") == 0:
        body = resp.get("body")
        set_secret(WITHINGS_ACCESS_TOKEN_SECRET, body.get("access_token"))
        set_secret(WITHINGS_REFRESH_TOKEN_SECRET, body.get("refresh_token"))
        set_secret(WITHINGS_USERID_SECRET, body.get("userid"))
        log.info("Tokens saved to Azure Key Vault")
        sync_last_7_days()
    else:
        log.warning(f"Token request failed with status {resp.get('status')}")
    return resp

def refresh_token_manual():
    client_id, client_secret = get_client_creds()
    refresh_token = get_secret(WITHINGS_REFRESH_TOKEN_SECRET)
    params = {
        "action": "requesttoken",
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }
    try:
        req = requests.post(TOKEN_URL, params)
        req.raise_for_status()
        resp = req.json()
    except requests.exceptions.RequestException as e:
        log.error(f"HTTP request failed: {e}")
        return None
    except ValueError as e:
        log.error(f"Failed to decode JSON response: {e}")
        return None
    if resp.get("status") == 0:
        body = resp.get("body")
        set_secret(WITHINGS_ACCESS_TOKEN_SECRET, body.get("access_token"))
        set_secret(WITHINGS_REFRESH_TOKEN_SECRET, body.get("refresh_token"))
        return body.get("access_token")
    log.warning(f"Refresh token request failed with status {resp.get('status')}")
    return None

class WithingsClient:
    def __init__(self):
        log.info("Loading Withings access token (access_token_secret=%s)", WITHINGS_ACCESS_TOKEN_SECRET)
        self.access_token = get_secret(WITHINGS_ACCESS_TOKEN_SECRET)

    def get_day_measures(self, day_str):
        target_date = datetime.strptime(day_str, "%Y-%m-%d").date()
        start_timestamp = time.mktime(target_date.timetuple())
        end_timestamp = time.mktime((target_date + timedelta(days=1)).timetuple()) - 1
        
        params = {
            "access_token": self.access_token,
            "category": 1,
            "startdate": start_timestamp,
            "enddate": end_timestamp,
        }
        req = requests.post(GET_MEASUREMENTS_URL, params)
        resp = req.json()
        
        if resp.get("status") != 0:
            new_token = refresh_token_manual()
            if new_token:
                self.access_token = new_token
                params["access_token"] = self.access_token
                req = requests.post(GET_MEASUREMENTS_URL, params)
                resp = req.json()
        
        if resp.get("status") != 0:
            return None
            
        return resp.get("body", {}).get("measuregrps", [])

def init_client():
    return WithingsClient()

def convert_measurement_value(value, unit):
    if unit == -3:
        return value / 1000.0
    elif unit == -2:
        return value / 100.0
    elif unit == -1:
        return value / 10.0
    else:
        return value

def fetch_day_data(client, day_str):
    measuregrps = client.get_day_measures(day_str)
    if not measuregrps:
        return None
    
    latest_date = 0
    latest_group = None
    for group in measuregrps:
        group_date = group.get("date", 0)
        if group_date > latest_date:
            latest_date = group_date
            latest_group = group
    
    if not latest_group:
        return None
    
    measures = latest_group.get("measures", [])
    
    data = {
        "date": day_str,
        "weight_kg": None,
        "fat_free_mass_kg": None,
        "fat_ratio_percent": None,
        "fat_mass_kg": None,
        "muscle_mass_kg": None,
        "hydration_kg": None,
        "bone_mass_kg": None,
    }
    
    for measure in measures:
        meas_type = measure.get("type")
        value = measure.get("value")
        unit = measure.get("unit", 0)
        converted_value = convert_measurement_value(value, unit)
        
        if meas_type == 1:
            data["weight_kg"] = converted_value
        elif meas_type == 5:
            data["fat_free_mass_kg"] = converted_value
        elif meas_type == 6:
            data["fat_ratio_percent"] = converted_value
        elif meas_type == 8:
            data["fat_mass_kg"] = converted_value
        elif meas_type == 76:
            data["muscle_mass_kg"] = converted_value
        elif meas_type == 77:
            data["hydration_kg"] = converted_value
        elif meas_type == 88:
            data["bone_mass_kg"] = converted_value
    
    return data

def sync_last_7_days():
    client = init_client()
    conn, cur = init_db()
    today = date.today()
    total_days = 7
    log.info("Starting Withings last_7_days sync")
    for i in range(total_days):
        day = today - timedelta(days=i)
        data = fetch_day_data(client, day.isoformat())
        if data:
            insert_data_withings(cur, conn, data)
            log.info(f"synced day {day.isoformat()} ({i + 1}/{total_days})")
        else:
            log.info(f"no data for day {day.isoformat()} ({i + 1}/{total_days})")
    cur.close()
    conn.close()
    log.info("Finished Withings last_7_days sync")

def sync_year():
    client = init_client()
    conn, cur = init_db()
    today = date.today()
    total_days = (today - START_DATE).days + 1
    log.info(f"Starting Withings year sync from {START_DATE.isoformat()} to {today.isoformat()}")
    
    for i in range(total_days):
        day = START_DATE + timedelta(days=i)
        data = fetch_day_data(client, day.isoformat())
        if data:
            insert_data_withings(cur, conn, data)
            log.info(f"synced day {day.isoformat()} ({i + 1}/{total_days})")
        else:
            log.info(f"no data for day {day.isoformat()} ({i + 1}/{total_days})")
    cur.close()
    conn.close()
    log.info("Finished Withings year sync")

def has_tokens():
    try:
        access = get_secret(WITHINGS_ACCESS_TOKEN_SECRET)
    except Exception:
        access = None
    try:
        refresh = get_secret(WITHINGS_REFRESH_TOKEN_SECRET)
    except Exception:
        refresh = None
    if access and refresh:
        return True
    missing = []
    if not access:
        missing.append(WITHINGS_ACCESS_TOKEN_SECRET)
    if not refresh:
        missing.append(WITHINGS_REFRESH_TOKEN_SECRET)
    log.warning(
        "Withings tokens missing; skipping sync (missing=%s). "
        "These secrets are expected to be created by the OAuth callback flow (/callback).",
        ", ".join(missing) if missing else "unknown",
    )
    return False

if __name__ == "__main__":
    sync_mode = os.environ.get("SYNC_MODE", "last_7_days")
    
    if sync_mode == "server":
        uvicorn.run(app, host="0.0.0.0", port=8081)
    elif sync_mode == "year":
        if has_tokens():
            sync_year()
    elif sync_mode == "last_7_days":
        if has_tokens():
            sync_last_7_days()
    else:
        uvicorn.run(app, host="0.0.0.0", port=8081)
