import pytest

from conftest import driver
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.product_page import ProductPage

@pytest.mark.usefixtures("driver")
class TestCartCount:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.product_page = ProductPage(driver)
        self.cart_page = CartPage(driver)
        self.driver.get("https://www.saucedemo.com/")
        self.login_page.login(username="standard_user", password="secret_sauce")

    @pytest.mark.full
    @pytest.mark.smoke
    @pytest.mark.order(1)
    def test_cart_empty_on_login(self):
        assert not self.product_page.is_element_visible(self.product_page.CART_BADGE)

    @pytest.mark.full
    @pytest.mark.smoke
    @pytest.mark.order(2)
    def test_add_one_product_by_index(self):
        self.product_page.add_product_by_index(0)
        assert self.product_page.get_cart_count() == 1

    @pytest.mark.full
    @pytest.mark.smoke
    @pytest.mark.order(3)
    def test_add_two_product_by_index(self):
        self.product_page.add_product_by_index(0)
        self.product_page.add_product_by_index(1)
        assert self.product_page.get_cart_count() == 2

    @pytest.mark.full
    @pytest.mark.smoke
    @pytest.mark.order(4)
    def test_remove_one_of_multiple_products(self):
        self.product_page.add_product_by_index(0)
        self.product_page.add_product_by_index(1)
        self.product_page.remove_product_by_index(0)
        assert self.product_page.get_cart_count() == 1

    @pytest.mark.full
    @pytest.mark.smoke
    @pytest.mark.order(5)
    def test_remove_all_products(self):
        self.product_page.add_product_by_index(0)
        self.product_page.add_product_by_index(1)
        self.product_page.remove_product_by_index(0)
        self.product_page.remove_product_by_index(1)
        assert not self.product_page.is_element_visible(self.product_page.CART_BADGE)

    @pytest.mark.full
    @pytest.mark.smoke
    @pytest.mark.order(6)
    def test_cart_navigation(self):
        self.product_page.add_product_by_index(0)
        self.product_page.go_to_cart()
        assert "cart.html" in self.driver.current_url

    @pytest.mark.full
    @pytest.mark.regression
    @pytest.mark.order(7)
    def test_remove_from_cart_page(self):
        self.product_page.add_product_by_index(0)
        self.product_page.add_product_by_index(1)
        self.product_page.go_to_cart()
        self.cart_page.remove_all_items()
        self.driver.back()
        assert not self.product_page.find_elements(self.product_page.CART_BADGE)

    @pytest.mark.full
    @pytest.mark.regression
    @pytest.mark.order(8)
    def test_cart_reset_after_logout(self):
        self.product_page.add_product_by_index(0)
        self.product_page.add_product_by_index(1)
        self.product_page.logout()
        self.login_page.login("standard_user", "secret_sauce")
        assert self.product_page.get_cart_count() == 2

