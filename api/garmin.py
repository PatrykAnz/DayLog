import os
import json
from garminconnect import Garmin
from pathlib import Path
from dotenv import load_dotenv
from utils.data_operations import load_json_data, save_json_data
from datetime import datetime

load_dotenv()

email = os.getenv("GARMIN_EMAIL")
password = os.getenv("GARMIN_PASSWORD")


def get_garmin():
    total_steps = 0
    total_sleep = 0

    api = Garmin(email, password)

    try:
        api.login()

        today = datetime.now().strftime("%Y-%m-%d")
        user_data = load_json_data("user_data.json")

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
        save_json_data("user_data.json", user_data)

    except Exception as e:
        print(f"Error getting Garmin data: {e}")
