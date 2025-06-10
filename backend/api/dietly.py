import os
import time

from backend.common.logging_config import logger
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from backend.common.config import (
    DIETLY_EMAIL,
    DIETLY_PASSWORD,
)
from backend.common.database import (
    execute_query,
    add_dietly_meal_to_table,
    check_dietly_meal_exists,
    add_meal_today_from_dietly,
    get_dietly_meal_by_id
)

load_dotenv()


def get_dietly():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    driver.get("https://dietly.pl/")
    wait = WebDriverWait(driver, 10)

    login_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[@class='button text-primary-500 h-[40px] ml-0 button-primary']//div[contains(text(), 'Zaloguj się')]",
            )
        )
    )
    login_button.click()

    write_email = wait.until(EC.element_to_be_clickable((By.ID, "email")))
    write_email.send_keys(DIETLY_EMAIL)
    write_password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    write_password.send_keys(DIETLY_PASSWORD)

    confirm_login = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[div[text()='Zaloguj']]"))
    )
    confirm_login.click()

    time.sleep(2)

    try:
        daily_summary = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".body-m.color-gray-700"))
        )
        logger.info("\nDaily Summary:")
        logger.info(daily_summary.text)
    except Exception as e:
        logger.error(f"Error getting daily summary: {e}")

    meal_elements = wait.until(
        EC.presence_of_all_elements_located(
            (
                By.CSS_SELECTOR,
                "li.DashboardMealsList_item__Sjtaa, li.DashboardMealsList_itemWithExcluded__kZZVh",
            )
        )
    )

    saved_meals = []
    
    for meal in meal_elements:
        try:
            meal_type = meal.find_element(By.CSS_SELECTOR, ".label-s").text.strip()
            meal_name = meal.find_element(
                By.CSS_SELECTOR, ".body-m.color-gray-900 span"
            ).text.strip()

            macros_div = meal.find_element(
                By.CSS_SELECTOR,
                ".display-flex.flex-wrap.align-items-center.body-m.color-gray-400",
            )
            macros_text = macros_div.text.strip()

            macro_parts = macros_text.split("•")
            kcal = float(macro_parts[0].strip().replace("kcal", "").strip().replace(",", "."))
            prot = float(macro_parts[1].strip().replace("B:", "").replace("g", "").strip().replace(",", "."))
            carbs = float(macro_parts[2].strip().replace("W:", "").replace("g", "").strip().replace(",", "."))
            fat = float(macro_parts[3].strip().replace("T:", "").replace("g", "").strip().replace(",", "."))

            existing_meal = check_dietly_meal_exists(meal_name)

            if existing_meal:
                logger.info(f"Meal '{meal_name}' already exists in dietly database")
                saved_meals.append(existing_meal)
            else:
                add_dietly_meal_to_table(meal_name, meal_type, kcal, prot, carbs, fat)
                logger.info(f"Added new meal to dietly database:")
                logger.info(f"Name: {meal_name}")
                logger.info(f"Type: {meal_type}")
                logger.info(f"Calories: {kcal}kcal")
                logger.info(f"Protein: {prot}g")
                logger.info(f"Carbs: {carbs}g")
                logger.info(f"Fat: {fat}g")
                
                new_meal = check_dietly_meal_exists(meal_name)
                if new_meal:
                    saved_meals.append(new_meal)
                    
        except Exception as e:
            logger.error(f"Error parsing meal: {e}")

    driver.quit()
    return saved_meals


def save_dietly_to_today():
    meals = get_dietly()
    
    if not meals:
        logger.warning("No meals found from Dietly")
        return
    
    logger.info("\nDietly meals saved to database!")
    logger.info("Now select how many grams of each meal you ate today:")
    
    for meal in meals:
        meal_id, name, tag, calories, protein, carbs, fat = meal
        
        logger.info(f"\nMeal: {name} ({tag})")
        logger.info(f"Calories: {calories}kcal, Protein: {protein}g, Carbs: {carbs}g, Fat: {fat}g")
        
        while True:
            try:
                grams_input = input("Enter grams consumed (or 'skip' to skip): ").strip().lower()
                
                if grams_input == 'skip':
                    logger.info(f"Skipped {name}")
                    break
                
                grams_consumed = float(grams_input)
                
                if grams_consumed >= 0:
                    if grams_consumed > 0:
                        add_meal_today_from_dietly(meal_id, grams_consumed)
                        logger.info(f"Added {grams_consumed}g of {name} to today's meals")
                    else:
                        logger.info(f"Skipped {name} (0g consumed)")
                    break
                else:
                    logger.info("Please enter a positive number")
                    
            except ValueError:
                logger.info("Please enter a valid number or 'skip'")
    
    logger.info("Finished adding Dietly meals to today's meals!")


if __name__ == "__main__":
    logger.info("test_file")
    save_dietly_to_today()
