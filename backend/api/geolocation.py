import geocoder
import json
from pathlib import Path
from backend.common.database import save_geolocation_data
from backend.common.logging_config import logger

def get_geolocation(city_name: str = None):
    if city_name:
        # Use provided city name
        g = geocoder.arcgis(city_name)
        if g.latlng:
            logger.info(f"Location set to {g.address}:")
            logger.info(f"Latitude: {g.latlng[0]}, Longitude: {g.latlng[1]}")

            # Save to database instead of JSON
            save_geolocation_data(
                latitude=g.latlng[0],
                longitude=g.latlng[1],
                address=g.address,
                city=city_name,
                country=g.country or ""
            )
            
            logger.info(f"Saved location data to database")
            return {
                "latitude": g.latlng[0],
                "longitude": g.latlng[1],
                "address": g.address,
                "city": city_name,
                "country": g.country or ""
            }
        else:
            logger.warning("Could not find coordinates for that city.")
            return None
    else:
        # Fallback to IP-based location
        g = geocoder.ip("me")
        if g.latlng:
            logger.info(f"Location set to {g.city}:")
            logger.info(f"Latitude: {g.latlng[0]}, Longitude: {g.latlng[1]}")

            # Save to database instead of JSON
            save_geolocation_data(
                latitude=g.latlng[0],
                longitude=g.latlng[1],
                address=g.address,
                city=g.city or "",
                country=g.country or ""
            )

            logger.info(f"Saved location data to database")
            return {
                "latitude": g.latlng[0],
                "longitude": g.latlng[1],
                "address": g.address,
                "city": g.city or "",
                "country": g.country or ""
            }
        else:
            logger.warning("Could not determine your location based on IP.")
            return None


if __name__ == "__main__":
    get_geolocation()
