from pathlib import Path

from api.garmin import get_garmin
from api.geolocation import get_geolocation
from api.weather import get_weather
from api.withings import get_withings
from common.data_operations import check_and_create_user_data
from common.logging_config import logger
from core.clock import get_clock
from core.event_calendar import get_calendar
from core.meals import get_meals
from core.notes import get_notes
from core.tasks import get_tasks
from core.workouts import get_workout

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
        9: "Workouts",
        10: "Meals",
        11: "Database"
        0: "Exit",
    }

    while True:
        logger.info("\nChoose an option:")
        for key, value in choices.items():

            logger.info(f"{key}. {value}")

        try:
            user_choice = int(input("\nYour choice: "))
            if user_choice in choices:
                if user_choice == 0:
                    return None

                logger.info(f"\n{choices[user_choice]}:")

                if user_choice == 1:
                    return get_weather()
                elif user_choice == 2:
                    return get_geolocation()
                elif user_choice == 3:
                    return get_clock()
                elif user_choice == 4:
                    return get_garmin()
                elif user_choice == 5:
                    return get_withings()
                elif user_choice == 6:
                    return get_notes()
                elif user_choice == 7:
                    return get_tasks()
                elif user_choice == 8:
                    return get_calendar()
                elif user_choice == 9:
                    return get_workout()
                elif user_choice == 10:
                    return get_meals()

                input("\nPress enter to return")
            else:
                logger.warning("Invalid choice. Please try again.")
                return None
        except ValueError:
            logger.error("Invalid input. Please enter a number.")


if __name__ == "__main__":
    get_user_choice()
