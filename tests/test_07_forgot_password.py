import pytest
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_forgot_password(driver):
    login_page = LoginPage(driver)
    login_page.go_to_login_page()

    # Click on "Forgot your password?" link
    login_page.click_forgot_password()

    # Enter a registered username
    registered_username = "testuser1"   # use an existing valid username
    login_page.enter_reset_username(registered_username)

    # Submit reset request
    login_page.submit_reset_request()

    # Wait for confirmation message
    wait = WebDriverWait(driver, 10)
    confirmation = wait.until(
        EC.presence_of_element_located((By.XPATH, "//h6[@class='oxd-text oxd-text--h6 orangehrm-forgot-password-title']"))
    )

    assert confirmation.is_displayed(), " Forgot password confirmation message not shown"
    print(" Forgot Password confirmation message displayed successfully")

    # Ensure redirected to reset password request page
    assert "sendPasswordReset" in driver.current_url, "User not redirected properly"
    print(" User redirected to password reset page")
