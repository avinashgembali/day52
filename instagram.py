from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

USERNAME = os.environ.get("username")
PASSWORD = os.environ.get("password")


class InstaFollower:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        self.driver.get(url="https://www.instagram.com/")

        time.sleep(2)
        username = self.driver.find_element(By.NAME, value="username")
        username.click()
        username.send_keys(USERNAME)
        username.send_keys(Keys.RETURN)

        password = self.driver.find_element(By.NAME, value="password")
        password.click()
        password.send_keys(PASSWORD)
        password.send_keys(Keys.RETURN)

        time.sleep(5)
        not_now = self.driver.find_element(By.XPATH, value="//div[text()='Not now']")
        not_now.click()

        # time.sleep(10)
        # turn_on = self.driver.find_element(By.XPATH, value="//button[text()='Turn On']")
        # turn_on.click()

    def find_followers(self):
        followers_url = "https://www.instagram.com/music___affair/followers/"
        self.driver.get(followers_url)
        time.sleep(5)
        followers = self.driver.find_element(By.XPATH, "//a[contains(@href, '/music___affair/followers/')]")
        followers.click()

        time.sleep(10)
        # Scroll through the popup
        scrollable_element = self.driver.find_element(By.XPATH, '//div[@style="height: auto; overflow: hidden auto;"]')

        # Function to scroll until reaching the bottom of the popup
        def scroll_popup(element):
            last_height = self.driver.execute_script("return arguments[0].scrollHeight", element)
            while True:
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)
                time.sleep(2)  # Wait for new followers to load
                new_height = self.driver.execute_script("return arguments[0].scrollHeight", element)
                if new_height == last_height:
                    break
                last_height = new_height

        scroll_popup(scrollable_element)

    def follow(self):
        # Find all "Follow" buttons in the popup
        follow_buttons = self.driver.find_elements(By.CSS_SELECTOR, value='div._ap3a._aaco._aacw._aad6._aade')

        # Click each "Follow" button
        for button in follow_buttons:
            try:
                button.click()
                time.sleep(1.1)
                # Clicking button for someone who is already being followed will trigger dialog to Unfollow/Cancel
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Cancel')]")
                cancel_button.click()
