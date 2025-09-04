# import necessary modules
# by for locating elements
#  webdriverwait and expected_conditions for waits
# exceptions for handling errors
# logger for logging
import os
from pydoc import text
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from utils.helpers import wait_for_visibility, wait_for_clickable
from utils.logger import get_logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# BasePage class to encapsulate common functionalities
class BasePage:
    # Constructor to initialize the driver, actions, logger, and base URL
    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(driver)
        self.log = get_logger(self.__class__.__name__)
        self.base_url = os.getenv("BASE_URL", "https://opensource-demo.orangehrmlive.com")
# Method to open a specific URL path
    def open(self, path: str = "/"):
        url = self.base_url.rstrip("/") + path
        self.log.info(f"Opening URL: {url}")
        self.driver.get(url)
        return self
# Method to find an element
    def find(self, locator):
        return wait_for_visibility(self.driver, locator)
# Method to click an element with handling for intercepted clicks
    def click(self, locator):
        try:
            elem = wait_for_clickable(self.driver, locator)
            elem.click()
        except ElementClickInterceptedException:
            self.log.info("Click intercepted, attempting JS click")
            elem = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].click();", elem)
# Method to type text into an input field
    def type(self, locator, text: str, clear_first=True):
        elem = wait_for_visibility(self.driver, locator)
        if clear_first:
            elem.clear()
        elem.send_keys(text)

# Method to check if an element is visible
    def is_visible(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except:
            return False

# Method to check if an element is present in the DOM
    def is_present(self, locator) -> bool:
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
