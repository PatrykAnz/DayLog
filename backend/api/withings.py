import os
import time
import requests
import json
from urllib.parse import urlencode
from backend.common.data_operations import ensure_data_folder, load_json_data, save_json_data
from backend.common.logging_config import logger
import webbrowser

CLIENT_ID = os.getenv("WITHINGS_CLIENT_ID")
CLIENT_SECRET = os.getenv("WITHINGS_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8080/callback"

TOKEN_URL = "https://wbsapi.withings.net/v2/oauth2"
API_ENDPOINT = "https://wbsapi.withings.net/measure"


def get_withings():
    if not CLIENT_ID or not CLIENT_SECRET:
        logger.info("Withings integration is not configured.")
        logger.info("To use Withings:")
        logger.info("1. Create a Withings developer account at: https://developer.withings.com/")
        logger.info("2. Create an app and get your Client ID and Secret")
        logger.info("3. Add these to your .env file:")
        logger.info("   WITHINGS_CLIENT_ID=your_client_id")
        logger.info("   WITHINGS_CLIENT_SECRET=your_client_secret")
        return {"status": "not_configured"}

    access_token = get_access_token()
    if not access_token:
        logger.error("Unable to get access token. Please check your Withings credentials.")
        return None
    
    response = requests.get(f"{API_ENDPOINT}?action=getmeas&meastype=1", 
                          headers={"Authorization": f"Bearer {access_token}"})
    
    if response.status_code == 200:
        try:
            data = response.json()
            if data.get("status") == 0 and data.get("body", {}).get("measuregrps"):
                latest_weight = data["body"]["measuregrps"][0]["measures"][0]["value"]
                weight_kg = latest_weight / 1000
                
                logger.info(f"Latest weight: {weight_kg:.1f} kg")
                
                user_data = load_json_data("backend.user_data.json")
                user_data["Withings"] = {"weight": weight_kg}
                save_json_data("backend.user_data.json", user_data)
                
                return {"weight": weight_kg}
            else:
                logger.warning("No weight data available")
                return None
        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Error parsing weight data: {e}")
            return None
    else:
        logger.error(f"Failed to get weight data: {response.text}")
        return None


def get_access_token():
    ensure_data_folder()
    
    token_data = load_json_data("withings_token.json")
    if token_data and "access_token" in token_data:
        if time.time() < token_data.get("expires_at", 0):
            return token_data["access_token"]
        elif "refresh_token" in token_data:
            return refresh_access_token(token_data["refresh_token"])
    
    auth_url = f"{TOKEN_URL}?" + urlencode({
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "user.metrics"
    })
    
    logger.info(f"Please visit this URL to authorize: {auth_url}")
    webbrowser.open(auth_url)
    
    code = input("Enter the authorization code: ")
    
    response = requests.post(TOKEN_URL, data={
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI
    })
    
    if response.status_code == 200:
        token_data = response.json()
        expires_in = token_data.get("expires_in", 3600)
        token_data["expires_at"] = time.time() + expires_in
        save_json_data("withings_token.json", token_data)
        return token_data.get("access_token")
    else:
        logger.error(f"Failed to get access token: {response.text}")
        return None


def refresh_access_token(refresh_token):        
    response = requests.post(TOKEN_URL, data={
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token
    })
    
    if response.status_code == 200:
        token_data = response.json()
        expires_in = token_data.get("expires_in", 3600)
        token_data["expires_at"] = time.time() + expires_in
        save_json_data("withings_token.json", token_data)
        return token_data.get("access_token")
    else:
        logger.error(f"Failed to refresh token: {response.text}")
        return None
