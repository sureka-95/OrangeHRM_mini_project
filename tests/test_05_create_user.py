# tests/test_add_employee_user.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages import admin_page
from pages.login_page import LoginPage
from pages.pim_page import PIMPage
from pages.admin_page import AdminPage
from pages.dashboard_page import DashboardPage
import time

@pytest.mark.usefixtures("driver")
class TestAddEmployeeUser:

    def test_add_employee_and_user_login(self, driver):
        wait = WebDriverWait(driver, 10)

        # 1. Login as Admin
        login_page = LoginPage(driver)
        login_page.login("Admin", "admin123")

        # 2. Add Employee in PIM
        pim_page = PIMPage(driver)
        pim_page.go_to_pim()
        employee_name = pim_page.add_employee("sum", "User123")

        # 3. Add System User in Admin
        admin_page = AdminPage(driver)
        admin_page.go_to_admin()
        username = "usersum"
        password = "user12345"
        admin_page.click_add_user()
        admin_page.select_user_role("ESS")
        admin_page.select_status("Enabled") 
        admin_page.add_user(employee_name, username, password)
        time.sleep(2)  # wait for toast

        dash = DashboardPage(driver)
        dash.logout()
        time.sleep(2)

        # Login as New User
        login_page = LoginPage(driver)
        login_page.login("usersum", "user12345")

        

        # Verify Dashboard appears
        assert wait.until(
            EC.presence_of_element_located((By.XPATH, "//h6[text()='Dashboard']"))
        ).is_displayed(), " New user login failed"
