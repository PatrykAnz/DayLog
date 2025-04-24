import geocoder

choices = {
    1: "Provide the name of the city",
    2: "Using IP (less accurate)"
}

def choose_geolocation():
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
            return g.latlng
        else:
            print("Could not find coordinates for that city.")
            return None
    elif user_choice == 2:
        g = geocoder.ip('me')
        if g.latlng:
            print(f"Location set to {g.city}:")
            print(f"Latitude: {g.latlng[0]}, Longitude: {g.latlng[1]}")
            return g.latlng
        else:
            print("Could not determine your location based on IP.")
            return None

if __name__ == "__main__":
    choose_geolocation()