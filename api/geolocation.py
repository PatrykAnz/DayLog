import geocoder
import json
from pathlib import Path

choices = {
    1: "Provide the name of the city",
    2: "Using IP (less accurate)",
}

def create_user_data(data_folder, data_file):
    if not data_folder.exists():
        data_folder.mkdir()
        print("Created 'user_data' folder.")
    
    if not data_file.exists():
        with open(data_file, "w") as f:
            json.dump({}, f)
        print("Created 'user_data.json' file.")

def geolocation():
    data_folder = Path("user_data")
    data_file = data_folder / "user_data.json"
    create_user_data(data_folder, data_file)
    
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
            
            with open(data_file, "w") as f:
                json.dump({"Geolocation": {"latitude": g.latlng[0], "longitude": g.latlng[1], "address": g.address}}, f, indent=4)
                print(f"Saved location data to {data_file}")
            return g.latlng
        else:
            print("Could not find coordinates for that city.")
            return None
    elif user_choice == 2:
        g = geocoder.ip('me')
        if g.latlng:
            print(f"Location set to {g.city}:")
            print(f"Latitude: {g.latlng[0]}, Longitude: {g.latlng[1]}")
            with open(data_file, "w") as f:
                json.dump({"Geolocation": {"latitude": g.latlng[0], "longitude": g.latlng[1], "address": g.address}}, f, indent=4)
                print(f"Saved location data to {data_file}")
            return g.latlng
        else:
            print("Could not determine your location based on IP.")
            return None

if __name__ == "__main__":
    geolocation()