import pytest
from pages.login_page import LoginPage
from utils.csv_data_reader import get_login_data_from_csv

@pytest.mark.parametrize("username,password,_", get_login_data_from_csv("data/valid_login_data.csv"))
def test_valid_login(driver, username, password, _):
    driver.get("https://www.saucedemo.com/")
    login_page = LoginPage(driver)
    login_page.login(username, password)
    assert "inventory" in driver.current_url