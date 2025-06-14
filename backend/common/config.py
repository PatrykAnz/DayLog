from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

# Base data folder 
DATA_FOLDER_NAME = "user_data"
DATA_FOLDER_PATH = Path(DATA_FOLDER_NAME)

DATABASE_MEALS_TABLE = "meals"

#DATABASE 
MAIN_DATABASE_FILE = "main.db"
MAIN_DATABASE_PATH = DATA_FOLDER_PATH / MAIN_DATABASE_FILE

# JSON data files
USER_DATA_FILE = "backend.user_data.json"
USER_MEALS_FILE = "user_meals.json"
USER_TASKS_FILE = "user_tasks.json"
USER_NOTES_FILE = "user_notes.json"
USER_CALENDAR_FILE = "user_calendar.json"
USER_WORKOUTS_FILE = "user_workouts.json"

# Withings 
WITHINGS_TOKEN_FILE = "withings_token.json"
WITHINGS_CREDS_FILE = "withings_creds.json"

# Dietly
DIETLY_EMAIL = os.getenv("DIETLY_EMAIL", "")
DIETLY_PASSWORD = os.getenv("DIETLY_PASSWORD", "")

# Garmin
GARMIN_EMAIL = os.getenv("GARMIN_EMAIL", "")
GARMIN_PASSWORD = os.getenv("GARMIN_PASSWORD", "")

#helper to check if the required envs are provided.
REQUIRED_ENVS = {
    "DIETLY_EMAIL": DIETLY_EMAIL,
    "DIETLY_PASSWORD": DIETLY_PASSWORD,
    "GARMIN_EMAIL": GARMIN_EMAIL,
    "GARMIN_PASSWORD": GARMIN_PASSWORD,
}

# Table names
TABLE_NOTES = "notes"
TABLE_TASKS = "tasks"
TABLE_CALENDAR = "calendar"
TABLE_WORKOUTS = "workouts"
TABLE_MEALS = "meals"
TABLE_MEALS_TODAY = "meals_today"
TABLE_DIETLY = "dietly"
TABLE_GELOCATION = "geolocation_data"
TABLE_WEATHER = "weather_data"
TABLE_GARMIN = "garmin_data"
TABLE_WITHINGS = "withings_data"
TABLE_API_TOKENS = "api_tokens"

def check_required_envs():
    """Log warnings if required environment variables are missing."""
    missing = [key for key, val in REQUIRED_ENVS.items() if not val]
    if missing:
        from backend.common.logging_config import logger 
        logger.warning(
            f"Missing environment variables: {', '.join(missing)}. Some features might not work as expected."
        )

check_required_envs() 
