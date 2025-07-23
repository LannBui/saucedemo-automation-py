import pytest
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.summary_page import SummaryPage
from pages.checkout_page import CheckoutPage

@pytest.mark.usefixtures("driver")
class TestCartAndSummaryPricesConsistent:
    @pytest.fixture(autouse=True)
    def setup_pages(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.product_page = ProductPage(driver)
        self.cart_page = CartPage(driver)
        self.summary_page = SummaryPage(driver)
        self.checkout_page = CheckoutPage(driver)
        self.driver.get("https://www.saucedemo.com/")
        self.login_page.login("standard_user", "secret_sauce")

    def test_cart_and_summary_prices_consistent(self):
        self.product_page.add_product_by_index(0)
        self.product_page.add_product_by_index(1)
        self.product_page.go_to_cart()
        cart_prices = self.cart_page.get_cart_item_prices()
        self.cart_page.click_checkout()
        self.checkout_page.enter_checkout_info("John", "Doe", "45678")
        self.checkout_page.click_continue()
        self.summary_page.wait_for_page()
        summary_prices = self.summary_page.get_summary_item_prices()
        assert cart_prices == summary_prices, f"Cart prices {cart_prices} do not match summary prices {summary_prices}" 