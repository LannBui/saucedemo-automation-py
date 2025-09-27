import pytest
from config.simple_config import config
from utils.driver_factory import get_driver

@pytest.fixture
def driver(request):
    # Get browser from config
    browser = config.browser
    
    # Command line options override config
    incognito = request.config.getoption("--incognito") or config.incognito
    headless = request.config.getoption("--headless") or config.headless
    
    driver = get_driver(browser_name=browser, incognito=incognito, headless=headless)
    
    # Set window size from config
    window_size = config.window_size
    driver.set_window_size(window_size[0], window_size[1])
    
    # Set timeouts from config
    driver.implicitly_wait(config.implicit_wait)
    driver.set_page_load_timeout(config.page_load_timeout)
    driver.set_script_timeout(config.script_timeout)
    
    yield driver
    driver.quit()

def pytest_addoption(parser):
    parser.addoption("--incognito", action="store_true", help="Run browser in incognito/private mode")
    parser.addoption("--headless", action="store_true", help="Run browser in headless mode")
    parser.addoption("--env", action="store", default="dev", help="Environment to run tests against (dev, staging, prod)")
