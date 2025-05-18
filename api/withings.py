import webbrowser
import requests
import time
from urllib.parse import urlencode, urlparse, parse_qs
from utils.data_operations import (
    load_json_data,
    save_json_data,
)
import datetime

TOKEN_FILE = "withings_token.json"
CREDS_FILE = "withings_creds.json"
USER_DATA_FILE = "user_data.json"

AUTH_URL = "https://account.withings.com/oauth2_user/authorize2"
TOKEN_URL = "https://wbsapi.withings.net/v2/oauth2"
API_ENDPOINT = "https://wbsapi.withings.net/measure"


def get_credentials():
    creds = load_json_data(CREDS_FILE)
    if (
        creds
        and "client_id" in creds
        and "client_secret" in creds
        and "callback_uri" in creds
    ):
        return creds

    client_id = input("Client ID: ")
    client_secret = input("Client Secret: ")
    callback_uri = input("Callback URI: ")

    creds = {
        "client_id": client_id,
        "client_secret": client_secret,
        "callback_uri": callback_uri,
    }

    save_json_data(CREDS_FILE, creds)
    return creds


def exchange_code_for_token(code, creds):
    token_params = {
        "action": "requesttoken",
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": creds["callback_uri"],
    }

    response = requests.post(TOKEN_URL, data=token_params)

    if response.status_code == 200:
        data = response.json()
        if data.get("status") == 0:
            token_data = data.get("body", {})
            token_data["created"] = int(datetime.datetime.now().timestamp())
            save_json_data(TOKEN_FILE, token_data)
            return token_data

    print(f"Error getting token: {response.text}")
    return None


def extract_code_from_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return query_params.get("code", [None])[0]


def refresh_token(refresh_token, creds):
    token_params = {
        "action": "requesttoken",
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }

    response = requests.post(TOKEN_URL, data=token_params)

    if response.status_code == 200:
        data = response.json()
        if data.get("status") == 0:
            token_data = data.get("body", {})
            token_data["created"] = int(datetime.datetime.now().timestamp())
            save_json_data(TOKEN_FILE, token_data)
            return token_data

    print("Error refreshing token")
    return None


def get_weight_data(token_data):

    creds = get_credentials()
    current_time = datetime.datetime.now().timestamp()

    if "expires_in" in token_data and current_time >= token_data.get(
        "created", 0
    ) + token_data.get("expires_in", 0):
        token_data = refresh_token(token_data.get("refresh_token"), creds)
        if not token_data:
            return None

    weight_params = {
        "action": "getmeas",
        "meastype": "1",
        "category": "1",
        "startdate": int(datetime.datetime.now().timestamp()) - (30 * 24 * 3600),
        "enddate": int(datetime.datetime.now().timestamp()),
        "access_token": token_data["access_token"],
    }

    response = requests.get(API_ENDPOINT, params=weight_params)

    if response.status_code == 200:
        data = response.json()
        if data.get("status") == 0:
            return data.get("body", {})

    print("Error getting weight data")
    return None


def get_withings():
    token_data = load_json_data(TOKEN_FILE)
    if token_data and "access_token" in token_data:
        print("Already authenticated")

        weight_data = get_weight_data(token_data)
        if weight_data:
            latest_weight = process_weight_data(weight_data)
            if latest_weight:

                save_weight_to_user_data(latest_weight)
        return token_data

    creds = get_credentials()

    auth_params = {
        "response_type": "code",
        "client_id": creds["client_id"],
        "redirect_uri": creds["callback_uri"],
        "scope": "user.info,user.metrics",
        "state": "withings_auth_state",
    }

    auth_url = f"{AUTH_URL}?{urlencode(auth_params)}"

    webbrowser.open(auth_url)

    callback_url = input("Paste the full callback URL here: ")

    auth_code = extract_code_from_url(callback_url)

    if auth_code:
        token_data = exchange_code_for_token(auth_code, creds)

        if token_data:
            print("Authsuccess")
            return token_data
        else:
            print("Access token error")
            save_json_data(CREDS_FILE, {})
            return None
    else:
        print("Something is wrong with the URL ")
        return None


def process_weight_data(weight_data):
    if "measuregrps" not in weight_data:
        print("No weight measurements found")
        return None

    measures = weight_data["measuregrps"]

    latest_date = None
    latest_weight = None

    sorted_measures = sorted(measures, key=lambda x: x.get("date", 0), reverse=True)

    for measure in sorted_measures:
        date = datetime.datetime.fromtimestamp(measure.get("date", 0))
        for measure_value in measure.get("measures", []):
            if measure_value.get("type") == 1:
                value = measure_value.get("value", 0) * (
                    10 ** measure_value.get("unit", 0)
                )

                if latest_date is None:
                    latest_date = date
                    latest_weight = value

    if latest_date and latest_weight:
        return {
            "date": latest_date.strftime("%Y-%m-%d"),
            "time": latest_date.strftime("%H:%M:%S"),
            "weight": round(latest_weight, 2),
            "units": "kg",
        }
    return None


def save_weight_to_user_data(weight_data):

    user_data = load_json_data(USER_DATA_FILE)

    if "Withings" not in user_data:
        user_data["Withings"] = {}

    user_data["Withings"]["weight"] = weight_data["weight"]
    user_data["Withings"]["units"] = weight_data["units"]
    user_data["Withings"]["date"] = weight_data["date"]

    save_json_data(USER_DATA_FILE, user_data)
    print(f"Saved today's weight: {weight_data['weight']} {weight_data['units']}")


if __name__ == "__main__":
    get_withings()
