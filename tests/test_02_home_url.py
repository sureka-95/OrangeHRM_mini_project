from pages.base_page import BasePage

def test_home_url_accessible(driver, base_url):
    BasePage(driver).open("/")
    assert base_url in driver.current_url
