import geocoder
import json
from pathlib import Path
from utils.data_operations import ensure_data_folder, load_json_data, save_json_data

choices = {
    1: "Provide the name of the city",
    2: "Using IP (less accurate)",
}


def get_geolocation():
    ensure_data_folder()
    user_data = load_json_data("user_data.json")

    print("Choose if you want to get it from city name or IP")
    for key, value in choices.items():
        print(f"{key}: {value}")
    user_choice = int(input(""))

    if user_choice == 1:
        city_name = input("Provide the name of the city: ")
        g = geocoder.arcgis(city_name)
        if g.latlng:
            print(f"Location set to {g.address}:")
            print(f"Latitude: {g.latlng[0]}, Longitude: {g.latlng[1]}")

            user_data["Geolocation"] = {
                "latitude": g.latlng[0],
                "longitude": g.latlng[1],
                "address": g.address,
            }

            save_json_data("user_data.json", user_data)
            print(f"Saved location data to user_data.json")
            return g.latlng
        else:
            print("Could not find coordinates for that city.")
            return None
    elif user_choice == 2:
        g = geocoder.ip("me")
        if g.latlng:
            print(f"Location set to {g.city}:")
            print(f"Latitude: {g.latlng[0]}, Longitude: {g.latlng[1]}")

            user_data["Geolocation"] = {
                "latitude": g.latlng[0],
                "longitude": g.latlng[1],
                "address": g.address,
            }

            save_json_data("user_data.json", user_data)
            print(f"Saved location data to user_data.json")
            return g.latlng
        else:
            print("Could not determine your location based on IP.")
            return None


if __name__ == "__main__":
    get_geolocation()
