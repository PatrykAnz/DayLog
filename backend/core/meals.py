from datetime import datetime
from backend.api.dietly import get_dietly
from common.data_operations import load_json_data, save_json_data
from common.logging_config import logger
from common.print_helpers import print_separator
from common.config import USER_MEALS_FILE


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
                logger.info("Choose between 1 or 2")
        except ValueError:
            logger.info("Choose between 1 or 2")
    while True:
        try:
            meal_kcal = int(input("Write kcal: "))
            break
        except ValueError:
            logger.info("Choose a valid number")
    while True:
        try:
            meal_fat = int(input("Write fat: "))
            break
        except ValueError:
            logger.info("Choose a valid number")
    while True:
        try:
            meal_carbs = int(input("Write carbs: "))
            break
        except ValueError:
            logger.info("Choose a valid number")
    while True:
        try:
            meal_protein = int(input("Write protein: "))
            break
        except ValueError:
            logger.info("Choose a valid number")
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
    meal_data = load_json_data(USER_MEALS_FILE)
    if not meal_data:
        logger.warning("No meals found")
        return
    print_separator()
    for i, meal in enumerate(meal_data, 1):
        logger.info(f"Meal {i}")
        logger.info(f"Name: {meal['Name']} ")
        logger.info(f"Tag: {meal['Tag']}")
        logger.info(f"Kcal: {meal['Kcal']}")
        logger.info(f"Protein: {meal['Protein']}")
        logger.info(f"Carbs: {meal['Carbs']}")
        logger.info(f"Fat: {meal['Fat']}")
        print_separator()


def update_meal():
    meal_data = load_json_data(USER_MEALS_FILE)
    if not meal_data:
        logger.warning("No meals to update")
    logger.info("Select which do you want to update")
    print_separator()
    for i, meal in enumerate(meal_data, 1):
        logger.info(f"Meal {i}")
        logger.info(f"Name: {meal['Name']} ")
        logger.info(f"Tag: {meal['Tag']}")
        logger.info(f"Kcal: {meal['Kcal']}")
        logger.info(f"Protein: {meal['Protein']}")
        logger.info(f"Carbs: {meal['Carbs']}")
        logger.info(f"Fat: {meal['Fat']}")
        print_separator()
    try:
        meal_to_update = int(input("Enter meal number to update (0 to cancel): ")) - 1
        if meal_to_update == -1:
            return
        if 0 <= meal_to_update < len(meal_data):
            logger.info("\nEnter new information (press Enter to keep current value):")
            new_name = (
                input(f"New name [{meal_data[meal_to_update]['Name']}]: ")
                or meal_data[meal_to_update]["Name"]
            )

            while True:
                try:
                    logger.info("1: 100g\n2: Meal")
                    new_tag = int(
                        input(f"New tag: [{meal_data[meal_to_update]['Tag']}]: ")
                        or meal_data[meal_to_update]["Tag"]
                    )

                    if new_tag == 1:
                        new_tag = "100g"
                        break
                    elif new_tag == 2:
                        new_tag = "Meal"
                        break
                    else:
                        logger.warning("Invalid choice. Please try again.")

                except ValueError:
                    logger.error("Invalid input. Please enter a number.")

            new_kcal = (
                input(f"New kcal [{meal_data[meal_to_update]['Kcal']}]: ")
                or meal_data[meal_to_update]["Kcal"]
            )
            new_protein = (
                input(f"New protein [{meal_data[meal_to_update]['Protein']}]: ")
                or meal_data[meal_to_update]["Protein"]
            )
            new_carbs = (
                input(f"New carbs [{meal_data[meal_to_update]['Carbs']}]: ")
                or meal_data[meal_to_update]["Carbs"]
            )
            new_fat = (
                input(f"New fat [{meal_data[meal_to_update]['Fat']}]: ")
                or meal_data[meal_to_update]["Fat"]
            )
            meal_data[meal_to_update].update(
                {
                    "Name": new_name,
                    "Tag": new_tag,
                    "Kcal": new_kcal,
                    "Protein": new_protein,
                    "Carbs": new_carbs,
                    "Fat": new_fat,
                }
            )
            logger.info(f"\nUpdated meal: {new_name}")
            save_json_data(USER_MEALS_FILE, meal_data)
        else:
            logger.warning("Invalid meal number!")
    except ValueError:
        logger.error("Please enter a valid number!")


def delete_meal():
    meal_data = load_json_data(USER_MEALS_FILE)
    if not meal_data:
        logger.warning("No meals to delete")

    logger.info("\nWhich meal would you like to delete?")
    print_separator()
    for i, meal in enumerate(meal_data, 1):
        logger.info(f"\n Meal #{i}")
        logger.info(f"Name: {meal['Name']}")
        logger.info(f"Tag: {meal['Tag']}")
        logger.info(f"Kcal: {meal['Kcal']}")
        logger.info(f"Protein: {meal['Protein']}")
        logger.info(f"Carbs: {meal['Carbs']}")
        logger.info(f"Fat: {meal['Fat']}")
        print_separator()

    try:
        meal_to_delete = int(input("Enter meal number to delete (0 to cancel): ")) - 1
        if meal_to_delete == -1:
            return
        if 0 <= meal_to_delete < len(meal_data):
            deleted_meal = meal_data.pop(meal_to_delete)
            logger.info(f"\nDeleted meal: {deleted_meal['Name']}")
            save_json_data(USER_MEALS_FILE, meal_data)
        else:
            logger.warning("Invalid meal number!")
    except ValueError:
        logger.error("Please enter a valid number!")


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
    logger.info("Save_dietly")
