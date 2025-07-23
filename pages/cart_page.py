from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    REMOVE_BUTTONS = (By.CLASS_NAME, "cart_button")
    CONTINUE_SHOPPING_BTN = (By.ID, "continue-shopping")
    CHECKOUT_BTN = (By.ID,"checkout")
    PRODUCT_PRICE_ELEMENTS = (By.CLASS_NAME, "inventory_item_price")

    def get_cart_item_count(self):
        return len(self.find_elements(self.CART_ITEMS))

    def remove_all_items(self):
        buttons = self.find_elements(self.REMOVE_BUTTONS)
        for button in buttons:
            button.click()

    def remove_product_by_index(self, index):
        buttons = self.find_elements(self.REMOVE_BUTTONS)
        buttons[index].click()

    def click_continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BTN)

    def click_checkout(self):
        self.click(self.CHECKOUT_BTN)

    def get_cart_item_prices(self):
        price_elements = self.driver.find_elements(*self.PRODUCT_PRICE_ELEMENTS)
        return [float(e.text.replace("$", "").strip()) for e in price_elements]




