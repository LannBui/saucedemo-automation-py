import pytest
import allure

from conftest import driver
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.product_page import ProductPage

@pytest.mark.usefixtures("driver")
@allure.epic("Cart Functionality")
@allure.feature("Cart Count and Operations")
class TestCartCount:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.product_page = ProductPage(driver)
        self.cart_page = CartPage(driver)
        with allure.step("Open Saucedemo homepage"):
            self.driver.get("https://www.saucedemo.com/")
        with allure.step("Login as standard_user"):
            self.login_page.login(username="standard_user", password="secret_sauce")

    @allure.story("Cart is empty on login")
    @allure.title("Cart should be empty after user logs in")
    @pytest.mark.full
    @pytest.mark.smoke
    @pytest.mark.order(1)
    def test_cart_empty_on_login(self):
        with allure.step("Verify cart badge is not visible"):
            assert not self.product_page.is_element_visible(self.product_page.CART_BADGE)

    @allure.story("Add one product to cart")
    @allure.title("Add one product by index and check cart count")
    @pytest.mark.full
    @pytest.mark.smoke
    @pytest.mark.order(2)
    def test_add_one_product_by_index(self):
        with allure.step("Add product at index 0 to cart"):
            self.product_page.add_product_by_index(0)
        with allure.step("Verify cart count is 1"):
            assert self.product_page.get_cart_count() == 1

    @allure.story("Add two products to cart")
    @allure.title("Add two products by index and check cart count")
    @pytest.mark.full
    @pytest.mark.smoke
    @pytest.mark.order(3)
    def test_add_two_product_by_index(self):
        with allure.step("Add product at index 0 to cart"):
            self.product_page.add_product_by_index(0)
        with allure.step("Add product at index 1 to cart"):
            self.product_page.add_product_by_index(1)
        with allure.step("Verify cart count is 2"):
            assert self.product_page.get_cart_count() == 2

    @allure.story("Remove one of multiple products")
    @allure.title("Remove one product and check cart count")
    @pytest.mark.full
    @pytest.mark.smoke
    @pytest.mark.order(4)
    def test_remove_one_of_multiple_products(self):
        with allure.step("Add product at index 0 to cart"):
            self.product_page.add_product_by_index(0)
        with allure.step("Add product at index 1 to cart"):
            self.product_page.add_product_by_index(1)
        with allure.step("Remove product at index 0 from cart"):
            self.product_page.remove_product_by_index(0)
        with allure.step("Verify cart count is 1"):
            assert self.product_page.get_cart_count() == 1

    @allure.story("Remove all products from cart")
    @allure.title("Remove all products and check cart is empty")
    @pytest.mark.full
    @pytest.mark.smoke
    @pytest.mark.order(5)
    def test_remove_all_products(self):
        with allure.step("Add product at index 0 to cart"):
            self.product_page.add_product_by_index(0)
        with allure.step("Add product at index 1 to cart"):
            self.product_page.add_product_by_index(1)
        with allure.step("Remove product at index 0 from cart"):
            self.product_page.remove_product_by_index(0)
        with allure.step("Remove product at index 1 from cart"):
            self.product_page.remove_product_by_index(1)
        with allure.step("Verify cart badge is not visible"):
            assert not self.product_page.is_element_visible(self.product_page.CART_BADGE)

    @allure.story("Cart navigation")
    @allure.title("Navigate to cart page and verify URL")
    @pytest.mark.full
    @pytest.mark.smoke
    @pytest.mark.order(6)
    def test_cart_navigation(self):
        with allure.step("Add product at index 0 to cart"):
            self.product_page.add_product_by_index(0)
        with allure.step("Go to cart page"):
            self.product_page.go_to_cart()
        with allure.step("Verify URL contains 'cart.html'"):
            assert "cart.html" in self.driver.current_url

    @allure.story("Remove from cart page")
    @allure.title("Remove all items from cart page and verify")
    @pytest.mark.full
    @pytest.mark.regression
    @pytest.mark.order(7)
    def test_remove_from_cart_page(self):
        with allure.step("Add product at index 0 to cart"):
            self.product_page.add_product_by_index(0)
        with allure.step("Add product at index 1 to cart"):
            self.product_page.add_product_by_index(1)
        with allure.step("Go to cart page"):
            self.product_page.go_to_cart()
        with allure.step("Remove all items from cart page"):
            self.cart_page.remove_all_items()
        with allure.step("Go back to products page"):
            self.driver.back()
        with allure.step("Verify cart badge is not visible"):
            assert not self.product_page.find_elements(self.product_page.CART_BADGE)

    @allure.story("Cart reset after logout")
    @allure.title("Cart should reset after logout and login again")
    @pytest.mark.full
    @pytest.mark.regression
    @pytest.mark.order(8)
    def test_cart_reset_after_logout(self):
        with allure.step("Add product at index 0 to cart"):
            self.product_page.add_product_by_index(0)
        with allure.step("Add product at index 1 to cart"):
            self.product_page.add_product_by_index(1)
        with allure.step("Logout user"):
            self.product_page.logout()
        with allure.step("Login again as standard_user"):
            self.login_page.login("standard_user", "secret_sauce")
        with allure.step("Verify cart count is 2"):
            assert self.product_page.get_cart_count() == 2

