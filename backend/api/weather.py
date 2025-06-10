import requests
import json
from backend.common.data_operations import ensure_data_folder, load_json_data, save_json_data
from backend.common.logging_config import logger


def get_weather():
    ensure_data_folder()
    user_data = load_json_data("backend.user_data.json")
    
    if "Geolocation" not in user_data:
        logger.warning("No geolocation data found. Please set your location first.")
        return None

    latitude = user_data["Geolocation"]["latitude"]
    longitude = user_data["Geolocation"]["longitude"]

    try:
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weathercode&timezone=auto"
        )

        response = requests.get(weather_url)
        weather_data = response.json()

        current = weather_data["current"]
        temperature = current["temperature_2m"]
        weather_code = current["weathercode"]

        weather_conditions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            95: "Thunderstorm",
        }

        condition = weather_conditions.get(weather_code, "Unknown")

        logger.info(f"Current temperature: {temperature}°C")
        logger.info(f"Weather condition: {condition}")

        user_data["Weather"] = {
            "temperature": temperature,
            "condition": condition,
            "weather_code": weather_code,
        }

        save_json_data("backend.user_data.json", user_data)
        logger.info("Weather data saved successfully!")

        return user_data["Weather"]

    except Exception as e:
        logger.error(f"Error fetching weather data: {e}")
        return None


if __name__ == "__main__":
    get_weather()
