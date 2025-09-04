# pages/dashboard_page.py
# import necessary modules
#   By for locating elements
#   EC for expected conditions
#   WebDriverWait for explicit waits
#  BasePage as the parent class
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# DashboardPage class inheriting from BasePage
class DashboardPage(BasePage):
   # Locators
    MENU_ITEMS = {
        "Admin": (By.XPATH, "//span[text()='Admin']"),
        "PIM": (By.XPATH, "//span[text()='PIM']"),
        "Leave": (By.XPATH, "//span[text()='Leave']"),
        "Time": (By.XPATH, "//span[text()='Time']"),
        "Recruitment": (By.XPATH, "//span[text()='Recruitment']"),
        "My Info": (By.XPATH, "//span[text()='My Info']"),
        "Performance": (By.XPATH, "//span[text()='Performance']"),
        "Dashboard": (By.XPATH, "//div[@class='oxd-topbar-header-title']"),
        "Directory": (By.XPATH, "//span[text()='Directory']"),
        "Maintenance": (By.XPATH, "//span[text()='Maintenance']"),
        "Claim": (By.XPATH, "//span[text()='Claim']"),
        "Buzz": (By.XPATH, "//span[text()='Buzz']"),
    }

    AVATAR_MENU = (By.CSS_SELECTOR, "span.oxd-userdropdown-tab")
    LOGOUT = (By.XPATH, "//a[text()='Logout']")

# Initialize with driver
    def __init__(self, driver):
        self.driver = driver

# define methods to check visibility of menu items
    def is_menu_item_visible(self, item_name="Dashboard", timeout=10):
        try:
            locator = self.MENU_ITEMS[item_name]
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element.is_displayed()
        except:
            return False
        
   # method to verify if logged in by checking dashboard header     
    def is_logged_in(self):
        self.dashboard_header = (By.XPATH, "//h6[text()='Dashboard']")
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.dashboard_header)
        ).is_displayed()

#  method to click on menu items
    def click_menu(self, name: str):
        self.click(self.MENU_ITEMS[name])
#  method to logout
    def logout(self):
        self.click(self.AVATAR_MENU)
        self.click(self.LOGOUT)
