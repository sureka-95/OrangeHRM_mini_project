from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



class LoginPage(BasePage):
    url = "https://opensource-demo.orangehrmlive.com"
    
    # Locators
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    BTN_LOGIN = (By.XPATH, "//button[@type='submit']")
    ERROR_MESSAGE = (By.XPATH, "//div[@class='oxd-alert-content oxd-alert-content--error']")
    LNK_FORGOT = (By.LINK_TEXT, "Forgot your password?")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def open_login(self):
        """Open the login page and maximize window"""
        self.driver.get(self.url)
        self.driver.maximize_window()
        return self
    
    def go_to_login_page(self):
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")


    def is_loaded(self):
        """Check that login page is fully loaded"""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.USERNAME)
            )
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.PASSWORD)
            )
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.BTN_LOGIN)
            )
            return True
        except TimeoutException:
            return False
        
    def login(self, username: str, password: str):
        """Perform login with given credentials"""
        # Ensure we are on login page
        if "orangehrmlive" not in self.driver.current_url:
            self.open_login()

        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.BTN_LOGIN)

        # Return DashboardPage on success
        from pages.dashboard_page import DashboardPage
        return DashboardPage(self.driver)

    def get_error_text(self):
        """Return error message text if login fails"""
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return element.text.strip()
        except TimeoutException:
            return ""

    def click_forgot_password(self):
        forgot_link = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//p[@class='oxd-text oxd-text--p orangehrm-login-forgot-header']"))
        )
        forgot_link.click()

    def enter_reset_username(self, username):
        input_box = self.wait.until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        input_box.clear()
        input_box.send_keys(username)

    def submit_reset_request(self):
        reset_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        reset_button.click()