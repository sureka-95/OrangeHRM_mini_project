from pages.admin_page import AdminPage
from pages.login_page import LoginPage
def test_validate_user_in_list(driver):
    
    login_page = LoginPage(driver)
    login_page.login("Admin", "admin123")

    admin_page = AdminPage(driver)
    admin_page.go_to_admin()

    # username created in test case 5
    username = "testuser1"

