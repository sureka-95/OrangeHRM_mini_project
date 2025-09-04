# pages/leave_page.py
# import necessary modules
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
import time

# class LeavePage inheriting from BasePage
class LeavePage(BasePage):
    # Initialize with driver
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    # Locators
    ASSIGN_LEAVE = (By.LINK_TEXT, "Assign Leave")
    EMPLOYEE_NAME_INPUT = (By.XPATH, "//input[@placeholder='Type for hints...']")
    SUGGESTION_OPTION = (By.XPATH, "//div[@role='listbox']//div[@role='option']")
    LEAVE_TYPE = (By.XPATH, "//div[@class='oxd-select-text-input']")
    LEAVE_TYPE_OPTION = (By.XPATH, "//div[@role='option']//span")
    FROM_DATE = (By.XPATH, "//label[text()='From Date']/../following-sibling::div//input")
    TO_DATE = (By.XPATH, "//label[text()='To Date']/../following-sibling::div//input")
    COMMENTS = (By.XPATH, "//label[text()='Comments']/../following-sibling::div//textarea")
    ASSIGN_BTN = (By.XPATH, "//button[@type='submit']")
    SUCCESS_TOAST = (By.XPATH, "//div[contains(@class,'oxd-toast-content')]//p[normalize-space()='Success']")
    LEAVE_RECORD_ROW = (By.XPATH, "//div[@class='oxd-table-body']//div[contains(text(),'CAN - Personal')]")
    OK_BTN = (By.XPATH, "//button[normalize-space()='Ok']")

    # Actions
    #   method to navigate to Assign Leave page
    def go_to_assign_leave(self):
        """Navigate to Assign Leave page"""
        self.wait.until(EC.element_to_be_clickable(self.ASSIGN_LEAVE)).click()

    #   method to enter employee name and select from suggestions    
    def enter_employee_name(self, employee_name):
        """Enter first 4 letters of employee name and select from suggestions"""
        emp_input = self.wait.until(EC.visibility_of_element_located(self.EMPLOYEE_NAME_INPUT))
        emp_input.clear()
        emp_input.send_keys(employee_name[:4])
        time.sleep(2)

        # Wait for suggestion list and pick the first one
        suggestions = self.wait.until(
            EC.visibility_of_all_elements_located(self.SUGGESTION_OPTION)
        )
        if suggestions:
            suggestions[0].click()
#   method to select leave type from dropdown
    def select_leave_type(self):
        """Select first available leave type"""
        self.wait.until(EC.element_to_be_clickable(self.LEAVE_TYPE)).click()
        self.wait.until(EC.element_to_be_clickable(self.LEAVE_TYPE_OPTION)).click()

    def set_date(self, locator, date_str):
        """Set date using JS executor (bypasses datepicker)"""
        elem = self.find(locator)
        self.driver.execute_script("arguments[0].click();", elem)
        self.driver.execute_script(
            "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));",
            elem,
            date_str
        )
#   method to enter comments
    def enter_comments(self, comment):
        """Enter comments in the textarea"""
        self.wait.until(EC.element_to_be_clickable(self.COMMENTS)).send_keys(comment)
#   method to click Assign button
    def click_assign(self):
        """Click Assign button"""
        self.wait.until(EC.element_to_be_clickable(self.ASSIGN_BTN)).click()
#   method to click OK button on success message
    def click_ok(self):
        """Click OK button on success message"""
        self.wait.until(EC.element_to_be_clickable(self.OK_BTN)).click()
#   method to perform full leave assignment workflow
    def assign_leave(self, employee_name, leave_type, from_date, to_date, comment):
        """Full workflow: assign leave to employee"""
        self.go_to_assign_leave()
        self.enter_employee_name(employee_name)
        self.select_leave_type()
        self.set_date(self.FROM_DATE, from_date)
        self.set_date(self.TO_DATE, to_date)
        self.enter_comments(comment)
        self.click_assign()
        self.click_ok()
#   method to get success message text
    def get_success_message(self):
        """Return success message after leave assignment"""
        try:
            element = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.SUCCESS_TOAST)
            )
            msg = element.text.strip()
            WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(self.SUCCESS_TOAST))
            return msg
        except TimeoutException:
            return ""

   