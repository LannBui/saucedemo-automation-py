import pytest
from pyexpat.errors import messages
import allure

from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.summary_page import SummaryPage
from pages.confirmation_page import ConfirmationPage

@pytest.mark.usefixtures("driver")
@allure.epic("Checkout")
@allure.feature("Checkout Flow")
class TestCheckoutFlow:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.product_page = ProductPage(driver)
        self.cart_page = CartPage(driver)
        self.checkout_page = CheckoutPage(driver)
        self.summary_page = SummaryPage(driver)
        self.confirmation_page = ConfirmationPage(driver)
        with allure.step("Open Saucedemo homepage"):
            self.driver.get("https://www.saucedemo.com/")
        with allure.step("Login as standard_user"):
            self.login_page.login("standard_user", "secret_sauce")

    @pytest.mark.order(1)
    @pytest.mark.smoke
    @pytest.mark.full
    def test_happy_path_checkout(self):
        self.product_page.add_product_by_index(0)
        self.product_page.add_product_by_index(1)
        self.product_page.go_to_cart()
        self.cart_page.click_checkout()
        self.checkout_page.enter_checkout_info("John", "Doe", "12345")
        self.checkout_page.click_continue()
        self.summary_page.click_finish()
        message = self.confirmation_page.get_confirmation_message()
        assert "Thank you for your order!" in message

    @pytest.mark.order(2)
    @pytest.mark.regression
    @pytest.mark.full
    def test_continue_shopping_step_one(self):
        self.product_page.add_product_by_index(0)
        self.product_page.add_product_by_index(1)
        self.product_page.go_to_cart()
        self.cart_page.click_continue_shopping()
        assert "inventory" in self.driver.current_url

    @pytest.mark.order(3)
    @pytest.mark.regression
    @pytest.mark.full
    def test_cancel_checkout_step_two(self):
        self.product_page.add_product_by_index(0)
        self.product_page.add_product_by_index(1)
        self.product_page.go_to_cart()
        self.cart_page.click_checkout()
        self.checkout_page.enter_checkout_info("John", "Doe", "45678")
        self.checkout_page.click_continue()
        self.checkout_page.click_cancel()
        assert "inventory.html" in self.driver.current_url

    @pytest.mark.order(4)
    @pytest.mark.regression
    @pytest.mark.full
    def test_cancel_checkout_step_one(self):
        self.product_page.add_product_by_index(0)
        self.product_page.add_product_by_index(1)
        self.product_page.go_to_cart()
        self.cart_page.click_checkout()
        self.checkout_page.enter_checkout_info("John", "Doe", "45678")
        self.checkout_page.click_cancel()
        assert "cart.html" in self.driver.current_url

    @pytest.mark.order(5)
    @pytest.mark.full
    def test_missing_checkout_info(self):
        self.product_page.add_product_by_index(0)
        self.product_page.add_product_by_index(1)
        self.product_page.go_to_cart()
        self.cart_page.click_checkout()
        self.checkout_page.enter_checkout_info("", "", "")
        self.checkout_page.click_continue()
        error = self.driver.find_element("xpath", "//h3[@data-test='error']").text
        assert "Error" in error


