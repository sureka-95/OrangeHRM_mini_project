from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class MyInfoPage(BasePage):
    MENU_ITEMS = {
        "Personal Details": (By.LINK_TEXT, "Personal Details"),
        "Contact Details": (By.LINK_TEXT, "Contact Details"),
        "Emergency Contacts": (By.LINK_TEXT, "Emergency Contacts"),
        "Dependents": (By.LINK_TEXT, "Dependents"),
        "Immigration": (By.LINK_TEXT, "Immigration"),
        "Job": (By.LINK_TEXT, "Job"),
        "Salary": (By.LINK_TEXT, "Salary"),
        "Tax Exemptions": (By.LINK_TEXT, "Tax Exemptions"),
        "Report-to": (By.LINK_TEXT, "Report-to"),
        "Qualifications": (By.LINK_TEXT, "Qualifications"),
        "Memberships": (By.LINK_TEXT, "Memberships"),
    }

    def menu_item_present(self, name: str) -> bool:
        return self.is_present(self.MENU_ITEMS[name])
