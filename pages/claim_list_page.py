# import necessary modules
# by for locating elements
# expected_conditions for waits
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# ClaimListPage class to encapsulate claim list page functionalities
class ClaimListPage:
    # Locators
    EMPLOYEE_CLAIMS_LINK = (By.LINK_TEXT, "Employee Claims")
    RESULT_ROWS = (By.XPATH, "//div[@class='oxd-table-body']//div[@role='row']")  
    RESULT_EMPLOYEE_NAME = (By.XPATH, ".//div[@role='cell'][2]")  # employee name cell, adjust index if needed

# Constructor to initialize the driver and wait
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
# Method to navigate to Employee Claims page
    def click_employee_claims(self):
        """Navigate to Employee Claims page"""
        self.wait.until(EC.element_to_be_clickable(self.EMPLOYEE_CLAIMS_LINK)).click()
# Method to validate if an employee exists in the claims list
    def validate_employee_in_claims(self, employee_name: str):
        """Check if employee name exists in the Employee Claims table"""
        rows = self.wait.until(EC.presence_of_all_elements_located(self.RESULT_ROWS))
        found = False
# Iterate through rows to find the employee
        for row in rows:
            name_cell = row.find_element(*self.RESULT_EMPLOYEE_NAME).text.strip()
            if employee_name.lower() in name_cell.lower():
                print(f" Found employee '{employee_name}' in claims list")
                found = True
                break
# assertion to ensure employee was found
        assert found, f"Employee {employee_name} not found in claims list"
        return True
