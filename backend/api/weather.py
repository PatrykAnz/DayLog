import requests
from api.geolocation import get_geolocation
from pathlib import Path
import json
from common.data_operations import check_and_create_user_data
from common.logging_config import logger


def get_weather():
    check_and_create_user_data()
    data_folder = Path("user_data")
    data_file = data_folder / "user_data.json"

    with open(data_file, "r") as f:
        user_data = json.load(f)

    if (
        "Geolocation" not in user_data
        or "latitude" not in user_data["Geolocation"]
        or "longitude" not in user_data["Geolocation"]
    ):
        get_geolocation()

        with open(data_file, "r") as f:
            user_data = json.load(f)

    latitude = user_data["Geolocation"]["latitude"]
    longitude = user_data["Geolocation"]["longitude"]

    request = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weathercode&timezone=auto"
    )
    weather_data = request.json()

    user_data["Weather"] = {
        "temperature": weather_data["current"]["temperature_2m"],
        "weathercode": weather_data["current"]["weathercode"],
        "time": weather_data["current"]["time"],
        "units": weather_data["current_units"]["temperature_2m"],
    }

    with open(data_file, "w") as f:
        json.dump(user_data, f, indent=4)

    logger.info(json.dumps(user_data, indent=4))
    logger.info(f"Weather data saved to {data_file}")
    
    return user_data["Weather"]


if __name__ == "__main__":
    get_weather()
