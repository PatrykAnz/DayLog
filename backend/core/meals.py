from datetime import datetime
from backend.api.dietly import get_dietly, save_dietly_to_today
from backend.common.data_operations import load_json_data, save_json_data
from backend.common.logging_config import logger
from backend.common.print_helpers import print_separator
from backend.common.config import USER_MEALS_FILE, DATABASE_MEALS_TABLE
from backend.common.database import (
    add_meal_to_table,
    check_name_from_table,
    read_last_rows_from_table,
    update_meal_in_table,
    get_meal_by_id,
    delete_meal_from_table,
    execute_query,
)


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

    meal_description = input("Write description (Can be skipped): ")
    if meal_description.strip() == "":
        meal_description = None

    add_meal_to_table(
        meal_name,
        meal_tag,
        meal_description,
        meal_kcal,
        meal_fat,
        meal_carbs,
        meal_protein,
        meal_mass,
    )

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
        meal_id, name, tag, description, calories, protein, carbs, fat, mass = meal

        logger.info(f"️Meal ID: {meal_id}")
        logger.info(f"Name: {name}")
        logger.info(f"Tag: {tag}")
        if description:
            logger.info(f"Description: {description}")
        else:
            logger.info(f"Description: no data")
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
        meal_id, name, tag, description, calories, protein, carbs, fat, mass = meal
        logger.info(f"Meal ID: {meal_id}")
        logger.info(f"Name: {name}")
        logger.info(f"Tag: {tag}")
        if description:
            logger.info(f"Description: {description}")
        else:
            logger.info(f"Description: no data")
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

        current_meal = get_meal_by_id(meal_id_to_update)
        if not current_meal:
            logger.warning("Meal ID not found!")
            return

        (
            meal_id,
            current_name,
            current_tag,
            current_description,
            current_calories,
            current_protein,
            current_carbs,
            current_fat,
            current_mass,
        ) = current_meal

        logger.info(f"\nUpdating meal: {current_name}")
        logger.info("Enter new information (press Enter to keep current value):")

        new_name_input = input(f"New name [{current_name}]: ")
        new_name = new_name_input if new_name_input.strip() else current_name

        description_display = current_description if current_description else "no data"
        new_description_input = input(
            f"New description [{description_display}]: (Can be skipped)"
        )
        new_description = (
            new_description_input
            if new_description_input.strip()
            else current_description
        )

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

        update_meal_in_table(
            meal_id_to_update,
            new_name,
            new_tag,
            new_description,
            new_calories,
            new_protein,
            new_carbs,
            new_fat,
            new_mass,
        )

        updated_meal = get_meal_by_id(meal_id_to_update)
        if updated_meal:
            logger.info(f"Meal '{new_name}' successfully updated in database!")
        else:
            logger.info("There was an error updating the meal")

    except ValueError:
        logger.error("Please enter a valid number!")


def delete_meal():
    meal_data = read_last_rows_from_table(DATABASE_MEALS_TABLE)
    if not meal_data:
        logger.warning("No meals to delete")
        return

    logger.info("Select which meal you want to delete:")
    print_separator()

    for meal in meal_data:
        meal_id, name, tag, description, calories, protein, carbs, fat, mass = meal
        logger.info(f"Meal ID: {meal_id}")
        logger.info(f"Name: {name}")
        logger.info(f"Tag: {tag}")
        if description:
            logger.info(f"Description: {description}")
        else:
            logger.info(f"Description: no data")
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
        meal_id_to_delete = int(input("Enter meal ID to delete (0 to cancel): "))
        if meal_id_to_delete == 0:
            return

        current_meal = get_meal_by_id(meal_id_to_delete)
        if not current_meal:
            logger.warning("Meal ID not found!")
            return

        meal_id, name, tag, description, calories, protein, carbs, fat, mass = (
            current_meal
        )

        logger.info(f"\nAre you sure you want to delete meal: {name}?")
        confirmation = input("Type 'yes' to confirm: ").lower()
        if confirmation != "yes":
            logger.info("Delete cancelled.")
            return

        delete_meal_from_table(meal_id_to_delete)

        deleted_check = get_meal_by_id(meal_id_to_delete)
        if not deleted_check:
            logger.info(f"Meal '{name}' successfully deleted from database!")
        else:
            logger.info("There was an error deleting the meal")

    except ValueError:
        logger.error("Please enter a valid number!")


def create_meal_today():
    logger.info("Creating meal entry for today:")
    meal_name = input("Write name of the meal: ")
    meal_data = check_name_from_table(DATABASE_MEALS_TABLE, meal_name)

    if not meal_data:
        try:
            user_choice = input(
                "No meals added with that name. Do you want to add a new meal?\n1: YES\n2: NO\n"
            )
            if user_choice == "1":
                create_meal()
                meal_data = check_name_from_table(DATABASE_MEALS_TABLE, meal_name)
                if not meal_data:
                    logger.warning("Meal was not created")
                    return
            elif user_choice == "2":
                return
            else:
                logger.info("Please choose 1 or 2")
                return
        except ValueError:
            logger.info("Please enter a valid number!")
            return

    logger.info("Meals found:")
    for i, meal in enumerate(meal_data):
        meal_id, name, tag, description, calories, protein, carbs, fat, mass = meal
        logger.info(f"{i + 1}. {name} ({tag}) - {calories} kcal")
        if description:
            logger.info(f"   Description: {description}")

    if len(meal_data) > 1:
        try:
            choice = int(input("Select meal number: ")) - 1
            if 0 <= choice < len(meal_data):
                selected_meal = meal_data[choice]
            else:
                logger.warning("Invalid selection!")
                return
        except ValueError:
            logger.error("Please enter a valid number!")
            return
    else:
        selected_meal = meal_data[0]

    meal_id, name, tag, description, calories, protein, carbs, fat, mass = selected_meal

    while True:
        try:
            percentage_input = input("Enter percentage eaten (0-100%): ").strip()
            percentage = float(percentage_input.replace('%', ''))
            
            if 0 <= percentage <= 100:
                if percentage > 0:
                    actual_calories = calories * percentage / 100
                    actual_protein = protein * percentage / 100
                    actual_carbs = carbs * percentage / 100
                    actual_fat = fat * percentage / 100
                    
                    execute_query(
                        """INSERT INTO meals_today 
                           (meal_id, meal_source, name, tag, calories, protein_grams, carbohydrates_grams, fat_grams, percentage) 
                           VALUES (?, 'manual', ?, ?, ?, ?, ?, ?, ?)""",
                        (meal_id, name, tag, actual_calories, actual_protein, actual_carbs, actual_fat, percentage)
                    )
                    
                    logger.info(f"Added {percentage}% of {name} ({tag}) to today's meals!")
                    logger.info(f"Consumed: {actual_calories:.1f} kcal, {actual_protein:.1f}g protein, {actual_carbs:.1f}g carbs, {actual_fat:.1f}g fat")
                else:
                    logger.info(f"Skipped {name} (0% eaten)")
                break
            else:
                logger.info("Please enter a percentage between 0 and 100")
        except ValueError:
            logger.info("Please enter a valid number!")


def read_meal_today():
    today_meals = execute_query("""
        SELECT id, meal_id, meal_source, name, tag, calories, protein_grams, carbohydrates_grams, fat_grams, time, percentage
        FROM meals_today
        WHERE DATE(time) = DATE('now')
        ORDER BY time DESC
    """)
    
    if not today_meals:
        logger.warning("No meals eaten today")
        return
    
    print_separator()
    logger.info("TODAY'S EATEN MEALS:")
    print_separator()
    
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    
    for meal in today_meals:
        entry_id, meal_id, source, name, tag, calories, protein, carbs, fat, time, percentage = meal
        
        total_calories += calories
        total_protein += protein
        total_carbs += carbs
        total_fat += fat
        
        logger.info(f"Entry ID: {entry_id}")
        logger.info(f"Meal: {name} ({tag})")
        logger.info(f"Source: {source}")
        logger.info(f"Time: {time}")
        logger.info(f"Percentage eaten: {percentage}%")
        logger.info(f"Consumed:")
        logger.info(f"  Calories: {calories:.1f} kcal")
        logger.info(f"  Protein: {protein:.1f}g")
        logger.info(f"  Carbs: {carbs:.1f}g")
        logger.info(f"  Fat: {fat:.1f}g")
        print_separator()
    
    logger.info("DAILY TOTALS:")
    logger.info(f"Total Calories: {total_calories:.1f} kcal")
    logger.info(f"Total Protein: {total_protein:.1f}g")
    logger.info(f"Total Carbs: {total_carbs:.1f}g")
    logger.info(f"Total Fat: {total_fat:.1f}g")
    print_separator()


def update_meal_today():
    today_meals = execute_query("""
        SELECT mt.id, mt.meal_id, mt.meal_source, mt.time, mt.percentage,
               CASE 
                   WHEN mt.meal_source = 'dietly' THEN d.name
                   ELSE m.name
               END as meal_name
        FROM meals_today mt
        LEFT JOIN meals m ON mt.meal_id = m.id AND mt.meal_source = 'manual'
        LEFT JOIN dietly d ON mt.meal_id = d.id AND mt.meal_source = 'dietly'
        WHERE DATE(mt.time) = DATE('now')
        ORDER BY mt.time DESC
    """)
    
    if not today_meals:
        logger.warning("No meals eaten today to update")
        return
    
    logger.info("Select which meal entry to update:")
    print_separator()
    
    for meal in today_meals:
        entry_id, meal_id, source, time, percentage, name = meal
        logger.info(f"Entry ID: {entry_id}")
        logger.info(f"Meal: {name} ({source})")
        logger.info(f"Time: {time}")
        logger.info(f"Current percentage: {percentage}%")
        print_separator()
    
    try:
        entry_id_to_update = int(input("Enter entry ID to update (0 to cancel): "))
        if entry_id_to_update == 0:
            return
        
        entry_exists = any(meal[0] == entry_id_to_update for meal in today_meals)
        if not entry_exists:
            logger.warning("Entry ID not found!")
            return
        
        while True:
            try:
                new_percentage_input = input("Enter new percentage (0-100%): ").replace('%', '')
                new_percentage = float(new_percentage_input)
                if 0 <= new_percentage <= 100:
                    execute_query(
                        "UPDATE meals_today SET percentage = ? WHERE id = ?",
                        (new_percentage, entry_id_to_update)
                    )
                    logger.info(f"Updated entry to {new_percentage}%")
                    break
                else:
                    logger.info("Please enter a percentage between 0 and 100")
            except ValueError:
                logger.info("Please enter a valid number")
                
    except ValueError:
        logger.error("Please enter a valid number!")


def delete_meal_today():
    today_meals = execute_query("""
        SELECT mt.id, mt.meal_id, mt.meal_source, mt.time, mt.percentage,
               CASE 
                   WHEN mt.meal_source = 'dietly' THEN d.name
                   ELSE m.name
               END as meal_name
        FROM meals_today mt
        LEFT JOIN meals m ON mt.meal_id = m.id AND mt.meal_source = 'manual'
        LEFT JOIN dietly d ON mt.meal_id = d.id AND mt.meal_source = 'dietly'
        WHERE DATE(mt.time) = DATE('now')
        ORDER BY mt.time DESC
    """)
    
    if not today_meals:
        logger.warning("No meals eaten today to delete")
        return
    
    logger.info("Select which meal entry to delete:")
    print_separator()
    
    for meal in today_meals:
        entry_id, meal_id, source, time, percentage, name = meal
        logger.info(f"Entry ID: {entry_id}")
        logger.info(f"Meal: {name} ({source})")
        logger.info(f"Time: {time}")
        logger.info(f"Percentage: {percentage}%")
        print_separator()
    
    try:
        entry_id_to_delete = int(input("Enter entry ID to delete (0 to cancel): "))
        if entry_id_to_delete == 0:
            return
        
        entry_exists = any(meal[0] == entry_id_to_delete for meal in today_meals)
        if not entry_exists:
            logger.warning("Entry ID not found!")
            return
        
        meal_name = next((meal[5] for meal in today_meals if meal[0] == entry_id_to_delete), "Unknown")
        
        logger.info(f"\nAre you sure you want to delete the entry for: {meal_name}?")
        confirmation = input("Type 'yes' to confirm: ").lower()
        if confirmation != "yes":
            logger.info("Delete cancelled.")
            return
        
        execute_query("DELETE FROM meals_today WHERE id = ?", (entry_id_to_delete,))
        logger.info(f"Successfully deleted meal entry!")
        
    except ValueError:
        logger.error("Please enter a valid number!")


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
                    save_dietly()
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
    save_dietly_to_today()
