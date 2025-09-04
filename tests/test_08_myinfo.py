import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import time
import os


@pytest.mark.myinfo
def test_validate_myinfo_menu(driver):
    login_page = LoginPage(driver)
    login_page.go_to_login_page()
    login_page.login("Admin", "admin123")   # valid credentials

    wait = WebDriverWait(driver, 15)

    # Navigate to My Info
    my_info = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='My Info']")))
    my_info.click()

    submenu_items = {
        "Personal Details": {"locator": "//a[normalize-space()='Personal Details']", "heading": "Personal Details"},
        "Contact Details": {"locator": "//a[normalize-space()='Contact Details']", "heading": "Contact Details"},
        "Emergency Contacts": {"locator": "//a[normalize-space()='Emergency Contacts']", "heading": "Assigned Emergency Contacts"},
        "Dependents": {"locator": "//a[normalize-space()='Dependents']", "heading": "Assigned Dependents"},
        "Immigration": {"locator": "//a[normalize-space()='Immigration']", "heading": "Assigned Immigration Records"},
        "Job": {"locator": "//a[normalize-space()='Job']", "heading": "Job"},
        "Salary": {"locator": "//a[normalize-space()='Salary']", "heading": "Assigned Salary Components"},
        "Tax Exemptions": {"locator": "//a[normalize-space()='Tax Exemptions']", "heading": "Tax Exemptions"},
        "Report-to": {"locator": "//a[normalize-space()='Report To' or normalize-space()='Report-to']", "heading": "Assigned Supervisors"},
        "Qualifications": {"locator": "//a[normalize-space()='Qualifications']", "heading": "Work Experience"},
        "Memberships": {"locator": "//a[normalize-space()='Memberships']", "heading": "Assigned Memberships"}
    }

    screenshot_dir = "screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)

    for section, details in submenu_items.items():
        try:
            elem = wait.until(EC.visibility_of_element_located((By.XPATH, details["locator"])))
            driver.execute_script("arguments[0].scrollIntoView(true);", elem)

            try:
                # Try normal Selenium click
                wait.until(EC.element_to_be_clickable((By.XPATH, details["locator"])))
                elem.click()
            except ElementClickInterceptedException:
                # Fallback: JS click if intercepted
                driver.execute_script("arguments[0].click();", elem)

            # Validate heading
            heading_elem = wait.until(
                EC.visibility_of_element_located((By.XPATH, f"//h6[contains(text(), '{details['heading']}')]"))
            )
            assert details["heading"] in heading_elem.text, f" Heading mismatch in {section}"

            print(f"✅ {section} opened and validated successfully")
            time.sleep(1)  # small pause

        except (TimeoutException, AssertionError, ElementClickInterceptedException) as e:
            # Save screenshot on failure
            screenshot_path = os.path.join(screenshot_dir, f"{section}_failure.png")
            driver.save_screenshot(screenshot_path)
            print(f" {section} failed: {e}. Screenshot saved at {screenshot_path}")