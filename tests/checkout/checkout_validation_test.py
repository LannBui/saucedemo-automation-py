import pytest
import allure
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.csv_data_reader import get_checkout_data_from_csv

@pytest.mark.usefixtures("driver")
@allure.epic("Checkout")
@allure.feature("Checkout Validations")
class TestCheckoutValidations:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.product_page = ProductPage(driver)
        self.cart_page = CartPage(driver)
        self.checkout_page = CheckoutPage(driver)
        with allure.step("Open Saucedemo homepage"):
            self.driver.get("https://www.saucedemo.com/")
        with allure.step("Login as standard_user"):
            self.login_page.login("standard_user", "secret_sauce")
        with allure.step("Add a product to cart"):
            self.product_page.add_product_by_index(0)
        with allure.step("Go to cart page"):
            self.product_page.go_to_cart()
        with allure.step("Click checkout"):
            self.cart_page.click_checkout()

    @allure.story("Checkout validation errors")
    @allure.title("Validate checkout form errors for missing/invalid data: {first_name}, {last_name}, {postal_code}")
    @pytest.mark.parametrize("first_name,last_name,postal_code,expected_error", get_checkout_data_from_csv("data/invalid_checkout_data.csv"))
    def test_checkout_validations(self, first_name, last_name, postal_code, expected_error):
        self.checkout_page.enter_checkout_info(first_name, last_name, postal_code)
        self.checkout_page.click_continue()
        error_msg = self.checkout_page.get_error_message_text()
        assert expected_error in error_msg


