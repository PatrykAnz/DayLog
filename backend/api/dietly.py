import os
import time

from common.logging_config import logger
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from common.config import (
    USER_MEALS_FILE,
    DIETLY_EMAIL,
    DIETLY_PASSWORD,
)
from common.data_operations import load_json_data

load_dotenv()

def get_dietly():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    # chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    driver.get("https://dietly.pl/")
    wait = WebDriverWait(driver, 10)

    # Login flow
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

    meals_data = []
    meal_data = load_json_data(USER_MEALS_FILE)
    for meal in meal_elements:
        try:
            meal_type = meal.find_element(By.CSS_SELECTOR, ".label-s").text.strip()
            meal_name = meal.find_element(
                By.CSS_SELECTOR, ".body-m.color-gray-900 span"
            ).text.strip()

            # Get all macro elements
            macros_div = meal.find_element(
                By.CSS_SELECTOR,
                ".display-flex.flex-wrap.align-items-center.body-m.color-gray-400",
            )
            macros_text = macros_div.text.strip()

            # Parse macros text
            macro_parts = macros_text.split("•")
            kcal = macro_parts[0].strip().replace("kcal", "").strip()
            prot = macro_parts[1].strip().replace("B:", "").replace("g", "").strip()
            carbs = macro_parts[2].strip().replace("W:", "").replace("g", "").strip()
            fat = macro_parts[3].strip().replace("T:", "").replace("g", "").strip()

            meal_data = {
                "Meal": meal_type,
                "Tag": "DIETA",
                "Name": meal_name,
                "Kcal": kcal,
                "Protein": prot,
                "Carbs": carbs,
                "Fat": fat,
            }
            meals_data.append(meal_data)

            logger.info(f"\n{meal_type}:")
            logger.info(f"Name: {meal_name}")
            logger.info(f"Calories: {kcal}kcal")
            logger.info(f"Protein: {prot}g")
            logger.info(f"Carbs: {carbs}g")
            logger.info(f"Fat: {fat}g")

        except Exception as e:
            logger.error(f"Error parsing meal: {e}")

    driver.quit()
    return meals_data


if __name__ == "__main__":
    logger.info("test_file")
    get_dietly()
