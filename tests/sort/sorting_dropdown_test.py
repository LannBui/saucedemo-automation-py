import pytest
from pages.login_page import LoginPage
from pages.product_page import ProductPage

@pytest.mark.usefixtures("driver")
class TestSortingDropdown:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.product_page = ProductPage(driver)
        self.driver.get("https://www.saucedemo.com/")
        self.login_page.login(username="standard_user", password="secret_sauce")

    @pytest.mark.parametrize("option", ["Name (A to Z)", "Name (Z to A)", "Price (low to high)", "Price (high to low)"])
    def test_sorting_dropdown(self, option):
        self.product_page.select_sort_option(option)

        if "Name" in option:
            names = self.product_page.get_product_names()
            sorted_names = sorted(names)
            if option == "Name (Z to A)":
                sorted_names.reverse()
            assert names == sorted_names, f"Expected {sorted_names}, got {names}"

        elif "Price" in option:
            prices = self.product_page.get_product_prices()
            sorted_prices = sorted(prices)
            if option == "Price (high to low)":
                sorted_prices.reverse()
            assert prices == sorted_prices, f"Expected {sorted_prices}, got {prices}"