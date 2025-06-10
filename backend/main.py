from pathlib import Path

from backend.api.garmin import get_garmin
from backend.api.geolocation import get_geolocation
from backend.api.weather import get_weather
from backend.api.withings import get_withings
from backend.common.data_operations import check_and_create_user_data
from backend.common.logging_config import logger
from backend.core.clock import get_clock
from backend.core.event_calendar import get_calendar
from backend.core.meals import get_meals
from backend.core.notes import get_notes
from backend.core.tasks import get_tasks
from backend.core.workouts import get_workout
from backend.common.database import get_database

from backend.user_data.transfer_meals import transfer_dietly_meals
data_folder = Path("user_data")
data_file = data_folder / "backend.user_data.json"


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
        11: "Database",
        12: "test",
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
                elif user_choice ==11:
                    return get_database()
                elif user_choice ==12:
                    return transfer_dietly_meals()

                input("\nPress enter to return")
            else:
                logger.warning("Invalid choice. Please try again.")
                return None
        except ValueError:
            logger.error("Invalid input. Please enter a number.")


if __name__ == "__main__":
    get_user_choice()
