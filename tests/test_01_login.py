import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

pytestmark = pytest.mark.login

def test_login_with_csv(driver, base_url, login_datasets):
    """
    Validate login using multiple credential sets from CSV.
    Logout after each successful login.
    """
    for username, password, expected in login_datasets:
        lp = LoginPage(driver)
        lp.open_login()
        assert lp.is_loaded(), "Login page not loaded"
        lp.login(username, password)

        if expected.strip().lower() == "success":
            dash = DashboardPage(driver)
            assert dash.is_menu_item_visible("Dashboard"), "Dashboard not visible after login"
            dash.logout()
        else:
            err = lp.get_error_text().lower()
            assert "invalid" in err or "credentials" in err, f"Expected invalid credentials error, got: {err}"
