import requests
import json
from backend.common.database import save_weather_data, execute_query
from backend.common.logging_config import logger
from backend.common.config import TABLE_GELOCATION


def get_weather():
    # Get the latest geolocation data from database
    geolocation_result = execute_query(f"SELECT latitude, longitude FROM {TABLE_GELOCATION} ORDER BY date DESC LIMIT 1")
    
    if not geolocation_result:
        logger.warning("No geolocation data found. Please set your location first.")
        return None

    latitude, longitude = geolocation_result[0]

    try:
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weathercode,relativehumidity_2m,windspeed_10m&timezone=auto"
        )

        response = requests.get(weather_url)
        weather_data = response.json()

        current = weather_data["current"]
        temperature = current["temperature_2m"]
        weather_code = current["weathercode"]
        humidity = current.get("relativehumidity_2m", 0)
        wind_speed = current.get("windspeed_10m", 0.0)

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
        logger.info(f"Humidity: {humidity}%")
        logger.info(f"Wind speed: {wind_speed} km/h")

        # Save to database instead of JSON
        location = f"{latitude}, {longitude}"
        save_weather_data(location, temperature, condition, humidity, wind_speed, weather_data)
        logger.info("Weather data saved successfully!")

        return {
            "temperature": temperature,
            "condition": condition,
            "weather_code": weather_code,
            "humidity": humidity,
            "wind_speed": wind_speed
        }

    except Exception as e:
        logger.error(f"Error fetching weather data: {e}")
        return None


if __name__ == "__main__":
    get_weather()
