import os
from pathlib import Path
from api.geolocation import get_geolocation
from api.weather import get_weather
from api.garmin import get_garmin
from utils.user_data_operations import check_and_create_user_data
from utils.clock import get_clock
from utils.notes import get_notes
from utils.separator import print_separator

data_folder = Path("user_data")
data_file = data_folder / "user_data.json"


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def get_user_choice():
    check_and_create_user_data()
    choices = {1: "Geolocation", 2: "Weather", 3: "Clock", 4: "Garmin", 5: "Notes"}
    total_amount = len(choices)
    while True:
        print(f"Choose from 1-{total_amount}")
        for key, value in choices.items():
            print(f"{key}. {value}")

        try:
            user_choice = int(input(""))
            if user_choice in choices:
                print(f"{choices[user_choice]}:")
                if user_choice == 1:
                    get_geolocation()
                elif user_choice == 2:
                    get_weather()
                elif user_choice == 3:
                    get_clock()
                elif user_choice == 4:
                    get_garmin()
                elif user_choice == 5:
                    get_notes()
                input("Press enter to return")
            else:
                print_separator()
                print("Invalid choice. Enter a number from the list.")
                print_separator()
        except ValueError as e:
            print_separator()
            print("An error has ocurred. Make sure you entered a number")
            print(f"\nError info: \n{e}")
            print_separator()


if __name__ == "__main__":
    get_user_choice()
