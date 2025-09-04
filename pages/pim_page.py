# pages/pim_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PIMPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Locators
    PIM_MENU = (By.XPATH, "//span[text()='PIM']")
    ADD_EMPLOYEE_BTN = (By.XPATH, "//a[text()='Add Employee']")
    FIRSTNAME_INPUT = (By.NAME, "firstName")
    LASTNAME_INPUT = (By.NAME, "lastName")
    SAVE_BTN = (By.XPATH, "//button[@type='submit']")
    EMPLOYEE_TABLE_ROWS = (By.CSS_SELECTOR, "div.oxd-table-body div.oxd-table-card")  
    EMPLOYEE_NAME_CELL = (By.CSS_SELECTOR, "div.oxd-table-body div.oxd-table-card div.oxd-table-cell:nth-child(3)")  
    # adjust nth-child index depending on where "Employee Name" column is

    def go_to_pim(self):
        self.wait.until(EC.element_to_be_clickable(self.PIM_MENU)).click()

    def add_employee(self, first_name, last_name):
        self.wait.until(EC.element_to_be_clickable(self.ADD_EMPLOYEE_BTN)).click()
        self.wait.until(EC.presence_of_element_located(self.FIRSTNAME_INPUT)).send_keys(first_name)
        self.driver.find_element(*self.LASTNAME_INPUT).send_keys(last_name)
        self.driver.find_element(*self.SAVE_BTN).click()

        # Wait until Employee Personal Details page loads
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h6[text()='Personal Details']")))
        return f"{first_name} {last_name}"

    def get_first_employee_name(self):
        # Wait until employee list is visible
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.EMPLOYEE_TABLE_ROWS)
        )
        # Get the first employee name in the list
        first_employee = self.driver.find_elements(*self.EMPLOYEE_NAME_CELL)[0].text.strip()
        return first_employee
    
    def is_employee_present(self, full_name):
        self.go_to_pim()
        try:
            # Search employee name in table
            rows = self.wait.until(
                EC.presence_of_all_elements_located(self.EMPLOYEE_NAME_CELL)
            )
            for row in rows:
                if row.text.strip() == full_name:
                    return True
            return False
        except:
            return False
