from tkinter.tix import Select

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

class ProductPage(BasePage):
    ADD_TO_CART_BUTTONS = (By.CLASS_NAME, "btn_inventory")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_ICON = (By.CLASS_NAME,"shopping_cart_link")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    PRODUCT_NAME_ELEMENTS = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICE_ELEMENTS = (By.CLASS_NAME, "inventory_item_price")

    # Logout
    MENU_NAVIGATION = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def add_product_by_index(self, index):
        buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        buttons[index].click()

    def remove_product_by_index(self, index):
        buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        buttons[index].click()

    def get_cart_count(self):
        if self.is_element_visible(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def go_to_cart(self):
        self.click(self.CART_ICON)

    def logout(self):
        self.click(self.MENU_NAVIGATION)
        self.click(self.LOGOUT_LINK)

    def select_sort_option(self, visible_text):
        self.select_by_visible_text(self.SORT_DROPDOWN, visible_text)

    def get_product_names(self):
        name_elements = self.driver.find_elements(*self.PRODUCT_NAME_ELEMENTS)
        return [e.text.strip() for e in name_elements]

    def get_product_prices(self):
        price_elements = self.driver.find_elements(*self.PRODUCT_PRICE_ELEMENTS)
        return [float(e.text.replace("$", "").strip()) for e in price_elements]



