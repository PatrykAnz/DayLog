import os
import json
from garminconnect import Garmin
from pathlib import Path
from dotenv import load_dotenv
from utils.user_data_operations import check_and_create_user_data
from datetime import datetime

load_dotenv()

data_file = Path("user_data") / "user_data.json"
email = os.getenv("GARMIN_EMAIL")
password = os.getenv("GARMIN_PASSWORD")


def get_garmin():
    check_and_create_user_data()
    
    total_steps = 0
    total_sleep = 0

    api = Garmin(email, password)

    try:
        api.login()

        today = datetime.now().strftime("%Y-%m-%d")

        with open(data_file, "r") as f:
            user_data = json.load(f)

        user_data["Garmin"] = {
            "steps": api.get_steps_data(today),
            "sleep": api.get_sleep_data(today),
        }

        for steps in user_data["Garmin"]["steps"]:
            total_steps += steps["steps"]

        sleep_data = user_data["Garmin"]["sleep"]["dailySleepDTO"]
        total_sleep = (
            sleep_data["deepSleepSeconds"]
            + sleep_data["lightSleepSeconds"]
            + sleep_data["remSleepSeconds"]
        )
        total_awake = sleep_data["awakeSleepSeconds"]

        aggregated_data = {
            "steps": total_steps,
            "sleep": total_sleep,
            "awake": total_awake
        }
        user_data["Garmin"] = aggregated_data
        with open(data_file, "w") as f:
            json.dump(user_data, f, indent=4)

    except Exception as e:
        print(f"Error getting Garmin data: {e}")
