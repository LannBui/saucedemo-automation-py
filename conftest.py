import pytest
from utils.driver_factory import get_driver

@pytest.fixture(params=["chrome"])
def driver(request):
    browser = request.param
    incognito = request.config.getoption("--incognito")
    headless = request.config.getoption("--headless")
    driver = get_driver(browser_name=browser, incognito=incognito, headless=headless)
    driver.maximize_window()
    yield driver
    driver.quit()

def pytest_addoption(parser):
    parser.addoption("--incognito", action="store_true", help="Run browser in incognito/private mode")
    parser.addoption("--headless", action="store_true", help="Run browser in headless mode")
