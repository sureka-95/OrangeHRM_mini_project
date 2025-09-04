from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

class DriverFactory:
    @staticmethod
    def get_driver(browser="chrome"):
        if browser.lower() == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-infobars")
            options.add_argument("--incognito")
            service = ChromeService(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=options)

        elif browser.lower() == "firefox":
            service = FirefoxService(GeckoDriverManager().install())
            return webdriver.Firefox(service=service)

        elif browser.lower() == "edge":
            service = EdgeService(EdgeChromiumDriverManager().install())
            return webdriver.Edge(service=service)

        else:
            raise ValueError(f"❌ Unsupported browser: {browser}")
