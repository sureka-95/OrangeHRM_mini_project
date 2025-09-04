from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

def test_menu_visibility_clickability_after_login(driver):
    LoginPage(driver).open_login().login("Admin", "admin123")
    dash = DashboardPage(driver)

    for name in ["Admin", "PIM", "Leave", "My Info", "Claim", "Dashboard"]:
        assert dash.is_menu_item_visible(name), f"Menu '{name}' not visible"
        dash.click_menu(name)  # clickability: no exception

    dash.logout()
