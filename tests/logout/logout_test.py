import pytest
from pages.login_page import LoginPage
from pages.product_page import ProductPage

@pytest.mark.usefixtures("driver")
class TestLogout:
    @pytest.fixture(autouse=True)
    def setup_pages(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.product_page = ProductPage(driver)
        self.driver.get("https://www.saucedemo.com/")
        self.login_page.login("standard_user", "secret_sauce")

    def test_logout(self):
        self.product_page.logout()
        assert "saucedemo.com" in self.driver.current_url