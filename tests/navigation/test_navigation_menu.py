import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

@pytest.mark.usefixtures("driver")
class TestNavigationMenu:
    @pytest.fixture(autouse=True)
    def setup_pages(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.product_page = ProductPage(driver)
        self.cart_page = CartPage(driver)
        self.driver.get("https://www.saucedemo.com/")
        self.login_page.login("standard_user", "secret_sauce")

    def open_menu(self):
        self.product_page.click(self.product_page.MENU_NAVIGATION)
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "logout_sidebar_link"))
        )

    @pytest.mark.order(1)
    @pytest.mark.full
    @pytest.mark.regression
    def test_all_items_link(self):
        self.open_menu()
        self.product_page.click(("id", "inventory_sidebar_link"))
        assert "inventory" in self.driver.current_url

    @pytest.mark.order(2)
    @pytest.mark.full
    @pytest.mark.regression
    def test_about_link(self):
        self.open_menu()
        self.product_page.click(("id", "about_sidebar_link"))
        WebDriverWait(self.driver,10).until(EC.url_contains("saucelabs.com"))
        assert "saucelabs.com" in self.driver.current_url

    @pytest.mark.order(3)
    @pytest.mark.full
    @pytest.mark.regression
    def test_reset_app_state(self):
        self.product_page.add_product_by_index(0)
        self.product_page.get_cart_count()
        assert self.product_page.get_cart_count() > 0
        self.open_menu()
        self.product_page.click(("id", "reset_sidebar_link"))
        self.product_page.get_cart_count()
        assert self.product_page.get_cart_count() == 0, "Cart is not empty after resetting app state"

    @pytest.mark.order(4)
    @pytest.mark.full
    @pytest.mark.smoke
    def test_logout_link(self):
        self.open_menu()
        self.product_page.click(("id", "logout_sidebar_link"))
        assert "saucedemo.com" in self.driver.current_url