import pytest
from pages.login_page import LoginPage
from utils.csv_data_reader import get_login_data_from_csv

@pytest.mark.full
@pytest.mark.regression
@pytest.mark.parametrize("username,password,expected_error", get_login_data_from_csv("data/invalid_login_data.csv"))
def test_invalid_login(driver, username, password, expected_error):
    driver.get("https://www.saucedemo.com/")
    login_page = LoginPage(driver)
    login_page.login(username, password)
    assert expected_error in login_page.get_error_message()