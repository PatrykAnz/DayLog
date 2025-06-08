from datetime import datetime
from backend.api.dietly import get_dietly
from common.data_operations import load_json_data, save_json_data
from common.logging_config import logger
from common.print_helpers import print_separator
from common.config import USER_MEALS_FILE, DATABASE_MEALS_TABLE 
from common.database import add_meal_to_table, check_name_from_table, read_last_rows_from_table, update_meal_in_table, get_meal_by_id

def create_meal():
    meal_name = input("Meal Name:")
    while True:
        try:
            kcal_choice = float(input("1: 100g\n2: Meal\n"))
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
            meal_kcal = float(input("Write kcal: "))
            break
        except ValueError:
            logger.info("Choose a valid number")
    while True:
        try:
            meal_fat = float(input("Write fat: "))
            break
        except ValueError:
            logger.info("Choose a valid number")
    while True:
        try:
            meal_carbs = float(input("Write carbs: "))
            break
        except ValueError:
            logger.info("Choose a valid number")
    while True:
        try:
            meal_protein = float(input("Write protein: "))
            break
        except ValueError:
            logger.info("Choose a valid number")
    while True:
        try:
            meal_mass_user_choice = input("Write mass: (Can be skipped)")
            if meal_mass_user_choice == "":
                meal_mass = None
                break
            else:
                meal_mass = float(meal_mass_user_choice)
                break
        except ValueError:
            logger.info("Choose a valid number")

    add_meal_to_table(meal_name, meal_tag, meal_kcal, meal_fat, meal_carbs, meal_protein, meal_mass)
    
    result = check_name_from_table(DATABASE_MEALS_TABLE, meal_name)
    if result:
        logger.info(f"RESULT: {result}")
        logger.info(f"Meal '{meal_name}' successfully added to database!")
    else: 
        logger.info(f"There was an error adding the meal")


def read_meal():
    meal_data = read_last_rows_from_table(DATABASE_MEALS_TABLE)
    if not meal_data:
        logger.warning("No meals found")
        return
    print_separator()
    logger.info("SAVED MEALS:")
    print_separator()
    
    for meal in meal_data:
        meal_id, name, tag, calories, protein, carbs, fat, mass = meal
        
        logger.info(f"️Meal ID: {meal_id}")
        logger.info(f"Name: {name}")
        logger.info(f"Tag: {tag}")
        logger.info(f"Calories: {calories} kcal")
        logger.info(f"Protein: {protein}g")
        logger.info(f"Carbohydrates: {carbs}g") 
        logger.info(f"Fat: {fat}g")
        if mass:
            logger.info(f"Mass: {mass}g")
        else:
            logger.info(f"Mass: no data")
        print_separator()

def update_meal():
    meal_data = read_last_rows_from_table(DATABASE_MEALS_TABLE)
    if not meal_data:
        logger.warning("No meals to update")
        return
        
    logger.info("Select which meal you want to update:")
    print_separator()
    
    for meal in meal_data:
        meal_id, name, tag, calories, protein, carbs, fat, mass = meal
        logger.info(f"Meal ID: {meal_id}")
        logger.info(f"Name: {name}")
        logger.info(f"Tag: {tag}")
        logger.info(f"Calories: {calories} kcal")
        logger.info(f"Protein: {protein}g")
        logger.info(f"Carbohydrates: {carbs}g")
        logger.info(f"Fat: {fat}g")
        if mass:
            logger.info(f"Mass: {mass}g")
        else:
            logger.info(f"Mass: no data")
        print_separator()
    
    try:
        meal_id_to_update = int(input("Enter meal ID to update (0 to cancel): "))
        if meal_id_to_update == 0:
            return
            
        # Check if meal exists
        current_meal = get_meal_by_id(meal_id_to_update)
        if not current_meal:
            logger.warning("Meal ID not found!")
            return
            
        meal_id, current_name, current_tag, current_calories, current_protein, current_carbs, current_fat, current_mass = current_meal
        
        logger.info(f"\nUpdating meal: {current_name}")
        logger.info("Enter new information (press Enter to keep current value):")
        
        # Get new name
        new_name_input = input(f"New name [{current_name}]: ")
        new_name = new_name_input if new_name_input.strip() else current_name
        
        # Get new tag
        while True:
            try:
                tag_input = input(f"Tag (1: 100g, 2: Meal) [{current_tag}]: ")
                if not tag_input.strip():
                    new_tag = current_tag
                    break
                tag_choice = int(tag_input)
                if tag_choice == 1:
                    new_tag = "100g"
                    break
                elif tag_choice == 2:
                    new_tag = "Meal"
                    break
                else:
                    logger.info("Choose between 1 or 2")
            except ValueError:
                logger.info("Choose between 1 or 2")
        
        # Get new calories
        while True:
            try:
                calories_input = input(f"New calories [{current_calories}]: ")
                if not calories_input.strip():
                    new_calories = current_calories
                    break
                new_calories = float(calories_input)
                break
            except ValueError:
                logger.info("Choose a valid number")
        
        # Get new protein
        while True:
            try:
                protein_input = input(f"New protein [{current_protein}]: ")
                if not protein_input.strip():
                    new_protein = current_protein
                    break
                new_protein = float(protein_input)
                break
            except ValueError:
                logger.info("Choose a valid number")
        
        # Get new carbs
        while True:
            try:
                carbs_input = input(f"New carbs [{current_carbs}]: ")
                if not carbs_input.strip():
                    new_carbs = current_carbs
                    break
                new_carbs = float(carbs_input)
                break
            except ValueError:
                logger.info("Choose a valid number")
        
        # Get new fat
        while True:
            try:
                fat_input = input(f"New fat [{current_fat}]: ")
                if not fat_input.strip():
                    new_fat = current_fat
                    break
                new_fat = float(fat_input)
                break
            except ValueError:
                logger.info("Choose a valid number")
        
        # Get new mass
        while True:
            try:
                mass_display = current_mass if current_mass else "no data"
                mass_input = input(f"New mass [{mass_display}]: (Can be skipped)")
                if not mass_input.strip():
                    new_mass = current_mass
                    break
                new_mass = float(mass_input) if mass_input else None
                break
            except ValueError:
                logger.info("Choose a valid number")
        
        # Update the meal in database
        update_meal_in_table(meal_id_to_update, new_name, new_tag, new_calories, new_protein, new_carbs, new_fat, new_mass)
        
        # Verify update was successful
        updated_meal = get_meal_by_id(meal_id_to_update)
        if updated_meal:
            logger.info(f"Meal '{new_name}' successfully updated in database!")
        else:
            logger.info("There was an error updating the meal")
            
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


def create_meals_today_table():
    print("test")


def create_meal_today():
    print("test")

def read_meal_today():
    print("test")


def update_meal_today():
    print("test")


def delete_meal_today():
    print("test")


def get_meals():
    choices = {
        1: "Create Meal",
        2: "Read Meal",
        3: "Update Meal",
        4: "Delete Meal",
        5: "Save todays Dietly",
        6: "Create Eaten Meal Today",
        7: "Read Eaten Meals Today",
        8: "Update Eaten Meal Today",
        9: "Delete Eaten Meal Today",
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
                elif user_choice == 2:
                    read_meal()
                elif user_choice == 3:
                    update_meal()
                elif user_choice == 4:
                    delete_meal()
                elif user_choice == 5:
                    save_json_data(USER_MEALS_FILE, get_dietly())
                elif user_choice == 6:
                    create_meal_today()
                elif user_choice == 7:
                    read_meal_today()
                elif user_choice == 8:
                    update_meal_today()
                elif user_choice == 9:
                    delete_meal_today()
                input("\nPress enter to return")
            else:
                logger.warning("Invalid choice. Please try again.")
                return None
        except ValueError:
            logger.error("Invalid input. Please enter a number.")


def save_dietly():
    logger.info("Save_dietly")
