from backend.api.dietly import get_dietly
from common.data_operations import get_file_path, load_json_data, save_json_data
from common.logging_config import logger

USER_MEALS_FILE = "user_meals.json"


def create_meal():
    meal_name = input("Meal Name:")
    while True:
        try:
            kcal_choice = int(input("1: 100g\n2: Meal\n"))
            if kcal_choice == 1:
                meal_tag = "100g"
                break
            elif kcal_choice == 2:
                meal_tag = "Meal"
                break
            else:
                print("Choose between 1 or 2")
        except ValueError:
            print("Choose between 1 or 2")

    while True:
        try:
            meal_kcal = int(input("Write kcal: "))
            break
        except ValueError:
            print("Choose a valid number")

    while True:
        try:
            meal_fat = int(input("Write fat: "))
            break
        except ValueError:
            print("Choose a valid number")

    while True:
        try:
            meal_carbs = int(input("Write carbs: "))
            break
        except ValueError:
            print("Choose a valid number")

    while True:
        try:
            meal_protein = int(input("Write protein: "))
            break
        except ValueError:
            print("Choose a valid number")

    meal_data = []
    meal_data = load_json_data(USER_MEALS_FILE)

    new_meal = {
        "Name": meal_name,
        "Tag": meal_tag,
        "Kcal": meal_kcal,
        "Protein": meal_protein,
        "Carbs": meal_carbs,
        "Fat": meal_fat,
    }

    meal_data.append(new_meal)
    save_json_data(USER_MEALS_FILE, meal_data)


def read_meal():
    print("read_meal")

    meal_data = load_json_data(USER_MEALS_FILE)
    if not meal_data:
        logger.warning("No meals found")
        return
    for i, meal in enumerate(meal_data, 1):
        logger.info(f"Meal {i}")
        logger.info(f"Name: {meal['name']} ")
        logger.info(f"")


def update_meal():
    print("Test")


def delete_meal():
    print("delete_meal")


def get_meals():
    choices = {
        1: "Create Meal",
        2: "Read Meal",
        3: "Update Meal",
        4: "Delete Meal",
        5: "Save todays Dietly",
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
                    create_meal()
                if user_choice == 2:
                    read_meal()
                if user_choice == 3:
                    update_meal()
                if user_choice == 4:
                    delete_meal()
                if user_choice == 5:
                    save_json_data(USER_MEALS_FILE, get_dietly())

                input("\nPress enter to return")
            else:
                logger.warning("Invalid choice. Please try again.")
                return None
        except ValueError:
            logger.error("Invalid input. Please enter a number.")


def save_dietly():
    print("Save_dietly")
