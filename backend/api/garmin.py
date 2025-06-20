import os
import json
from garminconnect import Garmin
from pathlib import Path
from dotenv import load_dotenv
from backend.common.config import GARMIN_EMAIL, GARMIN_PASSWORD
from backend.common.database import save_garmin_data
from datetime import datetime
from backend.common.logging_config import logger

load_dotenv()

email = GARMIN_EMAIL
password = GARMIN_PASSWORD


def get_garmin() -> dict:
    total_steps = 0
    total_sleep = 0
    total_awake = 0

    api = Garmin(email, password)

    try:
        api.login()

        today = datetime.now().strftime("%Y-%m-%d")

        steps_data = api.get_steps_data(today)
        sleep_data_raw = api.get_sleep_data(today)

        # Calculate total steps
        if steps_data:
            for steps in steps_data:
                if steps and "steps" in steps:
                    total_steps += steps["steps"] or 0

        # Calculate sleep totals
        if sleep_data_raw and "dailySleepDTO" in sleep_data_raw:
            sleep_data = sleep_data_raw["dailySleepDTO"]
            total_sleep = (
                (sleep_data.get("deepSleepSeconds") or 0) +
                (sleep_data.get("lightSleepSeconds") or 0) +
                (sleep_data.get("remSleepSeconds") or 0)
            )
            total_awake = sleep_data.get("awakeSleepSeconds") or 0

        aggregated_data = {
            "steps": total_steps,
            "sleep": total_sleep,
            "awake": total_awake,
        }
        
        logger.info(f"Total Steps: {total_steps}")
        logger.info(f"Total Sleep: {total_sleep} seconds ({total_sleep/3600:.2f} hours)")
        logger.info(f"Total Awake: {total_awake} seconds ({total_awake/3600:.2f} hours)")
        
        # Save to database instead of JSON
        save_garmin_data(total_steps, total_sleep, total_awake)
        
        return aggregated_data

    except Exception as e:
        logger.error(f"Error getting Garmin data: {e}")
        return {"error": str(e)}

