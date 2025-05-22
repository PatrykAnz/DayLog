import geocoder
import json
from pathlib import Path
from utils.data_operations import ensure_data_folder, load_json_data, save_json_data
from utils.logging_config import logger

def get_geolocation(city_name: str = None):
    ensure_data_folder()
    user_data = load_json_data("user_data.json")

    if city_name:
        # Use provided city name
        g = geocoder.arcgis(city_name)
        if g.latlng:
            logger.info(f"Location set to {g.address}:")
            logger.info(f"Latitude: {g.latlng[0]}, Longitude: {g.latlng[1]}")

            user_data["Geolocation"] = {
                "latitude": g.latlng[0],
                "longitude": g.latlng[1],
                "address": g.address,
            }

            save_json_data("user_data.json", user_data)
            logger.info(f"Saved location data to user_data.json")
            return user_data["Geolocation"]
        else:
            logger.warning("Could not find coordinates for that city.")
            return None
    else:
        # Fallback to IP-based location
        g = geocoder.ip("me")
        if g.latlng:
            logger.info(f"Location set to {g.city}:")
            logger.info(f"Latitude: {g.latlng[0]}, Longitude: {g.latlng[1]}")

            user_data["Geolocation"] = {
                "latitude": g.latlng[0],
                "longitude": g.latlng[1],
                "address": g.address,
            }

            save_json_data("user_data.json", user_data)
            logger.info(f"Saved location data to user_data.json")
            return user_data["Geolocation"]
        else:
            logger.warning("Could not determine your location based on IP.")
            return None


if __name__ == "__main__":
    get_geolocation()
