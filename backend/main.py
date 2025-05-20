from pathlib import Path
from api.geolocation import get_geolocation
from api.weather import get_weather
from api.garmin import get_garmin
from api.withings import get_withings
from utils.user_data_operations import check_and_create_user_data
from utils.clock import get_clock
from utils.notes import get_notes
from utils.print_helpers import print_separator, cls
from utils.tasks import get_tasks
from utils.event_calendar import get_calendar

data_folder = Path("user_data")
data_file = data_folder / "user_data.json"

def get_user_choice():
    check_and_create_user_data()
    choices = {
        1: "Weather", 
        2: "Geolocation", 
        3: "Clock", 
        4: "Garmin", 
        5: "Withings",
        6: "Notes",
        7: "Tasks",
        8: "Calendar",
        0: "Exit"
    }
    
    while True:
        print("\nChoose an option:")
        for key, value in choices.items():
            print(f"{key}. {value}")

        try:
            user_choice = int(input("\nYour choice: "))
            if user_choice in choices:
                if user_choice == 0:
                    return
                
                print(f"\n{choices[user_choice]}:")
                
                if user_choice == 1:
                    get_weather()
                elif user_choice == 2:
                    get_geolocation()
                elif user_choice == 3:
                    get_clock()
                elif user_choice == 4:
                    get_garmin()
                elif user_choice == 5:
                    get_withings()
                elif user_choice == 6:
                    get_notes()
                elif user_choice == 7:
                    get_tasks()
                elif user_choice == 8:
                    get_calendar()
                
                input("\nPress enter to return")
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    get_user_choice()
