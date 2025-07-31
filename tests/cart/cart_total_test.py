import pytest
import allure

from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.summary_page import SummaryPage

@pytest.mark.usefixtures("driver")
@allure.epic("Cart Functionality")
@allure.feature("Cart Totals")
class TestCartTotals:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.product_page = ProductPage(driver)
        self.cart_page = CartPage(driver)
        self.summary_page = SummaryPage(driver)
        self.checkout_page = CheckoutPage(driver)
        with allure.step("Open Saucedemo homepage"):
            self.driver.get("https://www.saucedemo.com/")
        with allure.step("Login as standard_user"):
            self.login_page.login("standard_user", "secret_sauce")

    @pytest.mark.full
    @pytest.mark.regression
    @pytest.mark.order(1)
    def test_item_total_updates_on_add(self):
        self.product_page.add_product_by_index(0)
        self.product_page.add_product_by_index(1)
        self.product_page.go_to_cart()
        item_prices = self.cart_page.get_cart_item_prices()
        expected_total = sum(item_prices)
        self.cart_page.click_checkout()
        self.checkout_page.enter_checkout_info("John", "Doe", "45678")
        self.checkout_page.click_continue()
        self.summary_page.wait_for_page()
        item_total = self.summary_page.get_item_total()
        assert item_total == expected_total, f"Expected {expected_total}, got {item_total}"

    @pytest.mark.full
    @pytest.mark.regression
    @pytest.mark.order(2)
    def test_item_total_updates_on_remove(self):
        self.product_page.add_product_by_index(0)
        self.product_page.add_product_by_index(1)
        self.product_page.go_to_cart()
        self.cart_page.remove_product_by_index(1)
        item_prices = self.cart_page.get_cart_item_prices()
        expected_total = sum(item_prices)
        self.cart_page.click_checkout()
        self.checkout_page.enter_checkout_info("John", "Doe", "45678")
        self.checkout_page.click_continue()
        self.summary_page.wait_for_page()
        item_total = self.summary_page.get_item_total()
        assert item_total == expected_total, f"Expected {expected_total}, got {item_total}"

    @pytest.mark.full
    @pytest.mark.regression
    @pytest.mark.order(3)
    def test_order_total_includes_tax(self):
        self.product_page.add_product_by_index(0)
        self.product_page.add_product_by_index(1)
        self.product_page.go_to_cart()
        self.cart_page.click_checkout()
        self.checkout_page.enter_checkout_info("John", "Doe", "45678")
        self.checkout_page.click_continue()
        self.summary_page.wait_for_page()
        item_total = self.summary_page.get_item_total()
        tax = self.summary_page.get_tax()
        order_total = self.summary_page.get_order_total()
        expected_total = item_total + tax
        assert abs(order_total - expected_total) < 0.01, f"Expected {expected_total}, got {order_total}"

    @pytest.mark.full
    @pytest.mark.regression
    @pytest.mark.order(4)
    def test_totals_with_empty_cart(self):
        self.product_page.go_to_cart()
        self.cart_page.click_checkout()
        self.checkout_page.enter_checkout_info("John", "Doe", "45678")
        self.checkout_page.click_continue()
        self.summary_page.wait_for_page()
        item_total = self.summary_page.get_item_total()
        order_total = self.summary_page.get_order_total()
        assert item_total == 0, f"Expected item total 0, got {item_total}"
        assert order_total == 0, f"Expected order total 0, got {order_total}" 