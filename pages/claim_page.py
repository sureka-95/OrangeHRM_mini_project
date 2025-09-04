# pages/claim_page.py
# import necessary modules
# By for locating elements
# EC for expected conditions
# webdriverwait for explicit waits
# ActionChains for advanced user interactions
# time for sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
import time

# ClaimPage class inheriting from BasePage
class ClaimPage(BasePage):
    # Locators
    CLAIM_MENU = (By.XPATH, "//span[text()='Claim']")
    ASSIGN_CLAIM_BTN = (By.XPATH, "//a[normalize-space()='Assign Claim']")
    EVENT_DROPDOWN = (By.XPATH, "//div[@class='oxd-select-text-input']")
    EVENT_OPTION = (By.XPATH, "//div[@role='option']//span[text()='Travel Allowance']")
    REMARKS_FIELD = (By.XPATH, "//textarea")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(text(),'Successfully Saved')]")
    CLAIM_HISTORY_ROWS = (By.XPATH, "//div[@class='oxd-table-card']")
    employee_name_input = (By.XPATH, "//input[@placeholder='Type for hints...']")
    currency_input = (By.XPATH, "//input[@placeholder='Currency']")
    SUGGESTION_OPTION = (By.XPATH, "//div[@role='option']")

# Initialize with driver
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
#   define methods for interactions
    def go_to_claim_section(self):
        """Navigate to Claim section"""
        menu = self.wait.until(EC.element_to_be_clickable(self.CLAIM_MENU))
        menu.click()
#   method to initiate a claim
    def initiate_claim(self, remarks: str):
        """Start new claim request"""
        claim_btn = self.wait.until(EC.element_to_be_clickable(self.ASSIGN_CLAIM_BTN))
        claim_btn.click()
    

        # Enter remarks
        remarks_box = self.wait.until(EC.visibility_of_element_located(self.REMARKS_FIELD))
        remarks_box.send_keys(remarks)

        # Submit
        submit_btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        submit_btn.click()

#   method to select currency from dropdown
    def select_currency(self, currency_name="Indian Rupee"):
        # Click currency dropdown
        dropdown = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//label[text()='Currency']/following::div[@class='oxd-select-text-input'][1]"))
        )
        dropdown.click()
        time.sleep(1)

        # Get all options in the dropdown
        options = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@role='option']//span"))
        )

        # Scroll and click the matching one
        for opt in options:
            if currency_name.lower() in opt.text.lower():
                self.driver.execute_script("arguments[0].scrollIntoView(true);", opt)
                opt.click()
                return True
        raise Exception(f"Currency '{currency_name}' not found in dropdown")

#   method to submit claim
    def submit_claim(self):
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        submit_button.click()

   # method to get employee name suggestions
    def enter_employee_name(self, employee_name: str):
        """Enter first 4 letters of employee name and select from suggestions"""
     # Enter employee name (first 4 chars)
        emp_input = self.wait.until(EC.visibility_of_element_located(self.employee_name_input))
        emp_input.clear()
        emp_input.send_keys(employee_name[:4])
        time.sleep(2)

        # Select first suggestion
        suggestion = self.wait.until(EC.visibility_of_element_located(self.SUGGESTION_OPTION))
        suggestion.click()
        dropdown = self.wait.until(EC.element_to_be_clickable(self.EVENT_DROPDOWN))
        dropdown.click()
        option = self.wait.until(EC.element_to_be_clickable(self.EVENT_OPTION))
        option.click()

    