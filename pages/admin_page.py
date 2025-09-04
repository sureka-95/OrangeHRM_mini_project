# pages/admin_page.py
# import necessary modules
# by for locating elements
#webdriverwait and expected_conditions for waits
# time for sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# AdminPage class to encapsulate admin page functionalities
class AdminPage:

    # Constructor to initialize the driver and wait
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Locators
        self.admin_tab = (By.XPATH, "//span[text()='Admin']")
        self.add_user_btn = (By.XPATH, "//button[normalize-space()='Add']")
        self.employee_name_input = (By.XPATH, "//input[@placeholder='Type for hints...']")
        self.username_input = (By.XPATH, "//label[text()='Username']/../following-sibling::div/input")
        self.password_input = (By.XPATH, "//label[text()='Password']/../following-sibling::div/input")
        self.confirm_password_input = (By.XPATH, "//label[text()='Confirm Password']/../following-sibling::div/input")
        self.save_button = (By.XPATH, "//button[@type='submit']")
        self.search_username_input = (By.XPATH, "//label[text()='Username']/../following-sibling::div/input")

        # Search button in the user management filter form
        self.search_button = (By.XPATH, "//div[@class='oxd-form-actions']//button[normalize-space()='Search']")
        self.user_role = (By.XPATH, "//div[contains(text(),'-- Select --')]")
        self.user_role_dropdown = (By.XPATH, "//label[text()='User Role']/../following-sibling::div//div[contains(@class,'oxd-select-text')]")
        self.user_role_option = lambda role: (By.XPATH, f"//div[@role='option']//span[text()='{role}']")
                # Status dropdown locators
        self.status_dropdown = (By.XPATH, "//label[text()='Status']/../following-sibling::div//div[contains(@class,'oxd-select-text')]")
        self.status_option = lambda status: (By.XPATH, f"//div[@role='option']//span[text()='{status}']")
        self.success_toast = (By.XPATH, "//div[contains(text(),'Successfully Saved')]")
        self.user_in_table = lambda username: (By.XPATH, f"//div[@role='table']//div[text()='{username}']")


    # Methods to interact with the page
    # Navigate to Admin tab
    def go_to_admin(self):
        self.wait.until(EC.element_to_be_clickable(self.admin_tab)).click()
    # Click Add User button
    def click_add_user(self):
        self.wait.until(EC.element_to_be_clickable(self.add_user_btn)).click()
    # Select user role from dropdown
    def select_user_role(self, role):
        # click dropdown
        self.wait.until(EC.element_to_be_clickable(self.user_role_dropdown)).click()
        # select option
        self.wait.until(EC.element_to_be_clickable(self.user_role_option(role))).click()
    # Select status from dropdown
    def select_status(self, status):
        self.wait.until(EC.element_to_be_clickable(self.status_dropdown)).click()
        self.wait.until(EC.element_to_be_clickable(self.status_option(status))).click()

# Add a new user
    def add_user(self, employee_name, username, password):
        emp_input = self.wait.until(EC.presence_of_element_located(self.employee_name_input))
        emp_input.send_keys(employee_name)
# Wait for and select the auto-suggested employee name
        suggestion = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='listbox']//span")))
        suggestion.click()
    # Fill in username, password, confirm password
        self.driver.find_element(*self.username_input).send_keys(username)
        time.sleep(1)
        self.driver.find_element(*self.password_input).send_keys(password)
        time.sleep(1)
        self.driver.find_element(*self.confirm_password_input).send_keys(password)
        time.sleep(1)
        self.driver.find_element(*self.save_button).click()
        

    def search_user(self, username):
    # Wait for Username input in search panel
        search_box = self.wait.until(EC.presence_of_element_located(self.search_username_input))
        search_box.clear()
        search_box.send_keys(username)

    # Click Search
        self.wait.until(EC.element_to_be_clickable(self.search_button)).click()

# Verify if user is present in the results table
    def is_user_present(self, username):
        # use try-except to handle case where user is not found
        try:
            result = self.wait.until(
                EC.presence_of_element_located((By.XPATH, f"//div[@role='table']//div[text()='{username}']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", result)
            return result.is_displayed()
        except:
            return False
