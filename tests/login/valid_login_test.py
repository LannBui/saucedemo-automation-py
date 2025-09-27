import pytest
from config.simple_config import config
from pages.login_page import LoginPage

@pytest.mark.full
@pytest.mark.smoke
@pytest.mark.login
@pytest.mark.critical
def test_valid_login(driver):
    # Get credentials from config
    username = config.username
    password = config.password

    driver.get(config.base_url)
    login_page = LoginPage(driver)
    login_page.login(username, password)
    assert "inventory" in driver.current_url