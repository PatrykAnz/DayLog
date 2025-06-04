from backend.api.dietly import get_dietly
from common.data_operations import get_file_path, load_json_data, save_json_data
from common.logging_config import logger
from common.config import USER_MEALS_FILE


def create_meal():
    print("create_meal")
    meal_name = input("Meal Name:")
    kcal_choice = int(input("1: 100g\n2: Meal"))
    if kcal_choice == 1:
        meal_tag = "100g"
    elif kcal_choice == 2:
        meal_tag = "Meal"
    else:
        return
    meal_kcal = input("Write kcal: ")
    meal_fat = input("Write fat:")
    meal_carbs = input("Write carbs: ")
    meal_protein = input("Write protein: ")
    meal_data = load_json_data(USER_MEALS_FILE)
    
    meal_data = []

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


def update_meal():
    print("update_meal")


def delete_meal():
    print("delete_meal")


def read_meal():
    print("read_meal")


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
