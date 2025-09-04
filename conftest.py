import csv
import os
import pytest
from dotenv import load_dotenv
from utils.driver_factory import DriverFactory
load_dotenv()


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="Browser to run tests on"
    )

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://opensource-demo.orangehrmlive.com")

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser") or "chrome"
    driver = DriverFactory.get_driver(browser)   # <-- fix here
    yield driver
    driver.quit()


# Data provider for CSV-driven login
@pytest.fixture(scope="session")
def login_datasets():
    path = os.path.join(os.path.dirname(__file__), "data", "login_data.csv")
    path = os.path.abspath(path)
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append((r["username"], r["password"], r["expected"]))
    return rows


import openpyxl

EXCEL_FILE = "test_results.xlsx"

def pytest_sessionstart(session):
    """Create Excel file and add headers at the start of the session"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Test Results"
    ws.append(["Test Name", "Result", "Duration (s)", "Error Message"])
    wb.save(EXCEL_FILE)

def pytest_runtest_logreport(report):
    """Log each test case result to Excel"""
    if report.when == "call":  # Only log actual test call (not setup/teardown)
        wb = openpyxl.load_workbook(EXCEL_FILE)
        ws = wb.active

        # Status
        if report.passed:
            result = "PASSED"
            error_msg = ""
        elif report.failed:
            result = "FAILED"
            error_msg = str(report.longrepr)[:200]  # capture first 200 chars of error
        else:
            result = "SKIPPED"
            error_msg = ""

        # Add row
        ws.append([report.nodeid, result, f"{report.duration:.2f}", error_msg])
        wb.save(EXCEL_FILE)
