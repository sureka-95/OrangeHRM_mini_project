from pages.login_page import LoginPage

def test_login_fields_present(driver):
    lp = LoginPage(driver).open_login()
    assert lp.is_loaded(), "Username, password or login button missing"
