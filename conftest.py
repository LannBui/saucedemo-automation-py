import pytest
from utils.driver_factory import get_driver

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser") or "chrome"
    driver = get_driver(browser)
    driver.maximize_window()
    yield driver
    driver.quit()

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to use for tests")
