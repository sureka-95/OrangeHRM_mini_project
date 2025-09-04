import pytest
from conftest import driver
from pages.login_page import LoginPage
from pages.claim_page import ClaimPage
from pages.claim_list_page import ClaimListPage
import time
from selenium.webdriver.support.ui import WebDriverWait
@pytest.mark.claim
def test_initiate_claim_request(driver):

    employee_name = "Jose ebert"

    # Login as employee
    login = LoginPage(driver)
    login.open_login().login("Admin", "admin123")

    # Navigate to claim section
    claim = ClaimPage(driver)
    claim.go_to_claim_section()

    # Initiate claim
    claim.initiate_claim("Business travel allowance")
    claim.enter_employee_name(employee_name)
    claim.select_currency("Indian Rupee")
    claim.submit_claim()

     # After submit, go to Employee Claims
   
    claim_list = ClaimListPage(driver, WebDriverWait(driver, 10))
    claim_list.click_employee_claims()

    assert claim_list.validate_employee_in_claims(employee_name), f"Employee {employee_name} not found in claim history table"

