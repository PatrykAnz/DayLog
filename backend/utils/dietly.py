import os
import re
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils.logging_config import logger
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()


DIETLY_EMAIL = os.getenv("DIETLY_EMAIL")
DIETLY_PASSWORD = os.getenv("DIETLY_PASSWORD")


def get_dietly():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

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

    # Extract meal data
    meal_elements = wait.until(
        EC.presence_of_all_elements_located(
            (
                By.CSS_SELECTOR,
                "li.DashboardMealsList_item__Sjtaa, li.DashboardMealsList_itemWithExcluded__kZZVh",
            )
        )
    )

    for meal in meal_elements:
        try:
            meal_type = meal.find_element(By.CSS_SELECTOR, ".label-s").text.strip()
            meal_name = meal.find_element(
                By.CSS_SELECTOR, ".body-m.color-gray-900 span"
            ).text.strip()
            macros = meal.find_elements(By.CSS_SELECTOR, ".body-m.color-gray-400 div")

            kcal = macros[0].text.strip().replace("kcal", "")
            prot = macros[2].text.strip().replace("B: ", "").replace("g", "")
            carbs = macros[4].text.strip().replace("W: ", "").replace("g", "")
            fat = macros[6].text.strip().replace("T: ", "").replace("g", "")

            return {
                "Meal": meal_type,
                "Name": meal_name,
                "Kcal": kcal,
                "Prot": prot,
                "Carbs": carbs,
                "Fat": fat,
            }

        except Exception as e:
            logger.error(f"Error parsing meal: {e}")


if __name__ == "__main__":
    logger.info("test_file")
    get_dietly()
