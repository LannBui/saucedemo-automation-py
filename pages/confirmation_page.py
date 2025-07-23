from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ConfirmationPage(BasePage):

    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def get_confirmation_message(self):
        return self.get_element_text(self.COMPLETE_HEADER)
