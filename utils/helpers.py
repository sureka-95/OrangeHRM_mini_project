from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

DEFAULT_TIMEOUT = 15

def wait_for_visibility(driver, locator, timeout: int = DEFAULT_TIMEOUT):
    try:
        return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))
    except TimeoutException as e:
        raise AssertionError(f"Element not visible: {locator}") from e

def wait_for_clickable(driver, locator, timeout: int = DEFAULT_TIMEOUT):
    try:
        return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
    except TimeoutException as e:
        raise AssertionError(f"Element not clickable: {locator}") from e

def wait_for_url_contains(driver, fragment: str, timeout: int = DEFAULT_TIMEOUT):
    try:
        WebDriverWait(driver, timeout).until(EC.url_contains(fragment))
        return True
    except TimeoutException:
        return False
