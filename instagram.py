from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

from dotenv import load_dotenv


load_dotenv()
username = os.getenv("INSTAGRAM_USERNAME")
password = os.getenv("INSTAGRAM_PASSWORD")
insgram_url = os.getenv("INSTAGRAM_URL")


driver = webdriver.Chrome()


def instagram_login():

    try:

        wait = WebDriverWait(driver, 15)

        driver.get(insgram_url)


        note = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//div[contains(text(), "First note in a while")]')
        ))


        note.click()

        input("Press Enter to close...")


        

    except Exception as e:
        print(f"An error occurred during Instagram login: {e}")




if __name__ == "__main__":
    instagram_login()  # Call the instagram_login function to start the program