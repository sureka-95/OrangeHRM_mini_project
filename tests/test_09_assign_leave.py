import pytest
import os
from pages.login_page import LoginPage
from pages.leave_page import LeavePage
from pages.leave_list_page import LeaveListPage
from pages.dashboard_page import DashboardPage
from selenium.webdriver.support.ui import WebDriverWait
import time


@pytest.mark.leave
def test_assign_leave_and_verify(driver):
    """
    Test Scenario:
    Assign leave to an employee and verify it appears in Leave List.
    Steps:
        1. Login as Admin/HR
        2. Navigate to Leave -> Assign Leave
        3. Fill required fields (employee name, leave type, duration, comment)
        4. Submit form
        5. Verify success message
        6. Navigate to Leave List
        7. Search by employee name and date
        8. Validate leave is recorded
    """

    employee_name = "Jose Ebert"
    leave_type = "CAN - Personal"      # Adjust per system
    from_date = "2025-09-05"
    to_date = "2025-09-05"
    comment = "personal work"

    # Step 1: Login
    login = LoginPage(driver)
    login.open_login().login("Admin", "admin123")
    dash = DashboardPage(driver)
    dash.click_menu("Leave")

    # Step 2: Navigate to Assign Leave
    leave = LeavePage(driver)
   

    # Step 3: Fill Leave Form
    leave.assign_leave(employee_name, leave_type, from_date, to_date, comment)

    # Step 4: Verify Success Message
    success_msg = leave.get_success_message()
    assert "Success" in success_msg, f"Leave assignment failed. Got: {success_msg}"

    wait = WebDriverWait(driver, 10)
    leave_list_page = LeaveListPage(driver, wait)
    leave_list_page.click_leave_list()
    time.sleep(2)
    leave_list_page.search_leave_by_employee(employee_name)
    leave_list_page.select_status_taken()
    leave_list_page.click_search()
    time.sleep(2)
    leave_list_page.validate_search_results(employee_name)
    dash.logout()
