import pyautogui # types keys, blindly
import pyperclip
import os
import time
import webbrowser # opens pages
from dotenv import load_dotenv


load_dotenv()
username = os.getenv("INSTAGRAM_USERNAME")
password = os.getenv("INSTAGRAM_PASSWORD")
insgram_url = os.getenv("INSTAGRAM_URL")


def instagram_login():

    # Open Instagram in the default browser (this actually launches/focuses it)
    webbrowser.open(insgram_url)
    time.sleep(5)  # Wait for the page to load


    pyperclip.copy(username)  # Copy the username to clipboard
    pyautogui.hotkey("ctrl", "v")  # Paste the username
    pyautogui.press("tab")  # Move to the password field
    pyperclip.copy(password)  # Copy the password to clipboard
    pyautogui.hotkey("ctrl", "v")  # Paste the password
    pyautogui.press("enter")  # Press Enter to log in






if __name__ == "__main__":
    instagram_login()  # Call the instagram_login function to start the program