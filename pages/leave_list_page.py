from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import Select

class LeaveListPage:
    # Locators
    EMPLOYEE_INPUT = (By.XPATH, "//input[@placeholder='Type for hints...']")
    SUGGESTION_OPTION = (By.XPATH, "//div[@role='option']")
    
    RESULT_ROWS = (By.XPATH, "//div[@class='oxd-table-body']//div[@role='row']")  # rows in results
    RESULT_EMPLOYEE_NAME = (By.XPATH, ".//div[@role='cell'][2]")  # employee name cell (adjust index if different)
    
    STATUS_DROPDOWN = (By.XPATH, "//div[@class='oxd-select-text-input']")
    STATUS_OPTION_TAKEN = (By.XPATH, "//div[@role='option']//span[text()='Taken']")
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit']")

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def click_leave_list(self):
        """Navig    ate to Leave List page"""
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Leave List"))).click()

    def search_leave_by_employee(self, employee_name: str):
        """Enter employee name, pick suggestion, select Taken status, and search"""
        # Enter employee name (first 4 chars)
        emp_input = self.wait.until(EC.visibility_of_element_located(self.EMPLOYEE_INPUT))
        emp_input.clear()
        emp_input.send_keys(employee_name[:4])
        time.sleep(2)

        # Select first suggestion
        suggestion = self.wait.until(EC.visibility_of_element_located(self.SUGGESTION_OPTION))
        suggestion.click()

#   method to select 'Taken' status from dropdown
    def select_status_taken(self):
        """Click status dropdown and choose 'Taken'"""
        dropdown = self.wait.until(EC.element_to_be_clickable(self.STATUS_DROPDOWN))
        dropdown.click()

        option = self.wait.until(EC.element_to_be_clickable(self.STATUS_OPTION_TAKEN))
        option.click()
#   method to click search button
    def click_search(self):
        """Click search button"""
        search_btn = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON))
        search_btn.click()

#   method to validate if employee name exists in results
    def validate_search_results(self, employee_name: str):
        """Check if employee name exists in the results"""
        rows = self.wait.until(EC.presence_of_all_elements_located(self.RESULT_ROWS))
        found = any(employee_name in row.text for row in rows)

        assert found, f"Employee {employee_name} not found in search results."
        return True