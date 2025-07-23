from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.csv_data_reader import get_login_data_from_csv


class SummaryPage(BasePage):
    SUMMARY_INFO_BOX = (By.CLASS_NAME, "summary_info")
    ITEM_TOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    ORDER_TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BTN = (By.ID, "finish")
    CANCEL_BTN = (By.ID, "cancel")

    def wait_for_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SUMMARY_INFO_BOX)
        )

    def get_item_total(self):
        text = self.driver.find_element(*self.ITEM_TOTAL_LABEL).text
        return float(text.split("$")[-1])

    def get_tax(self):
        text = self.driver.find_element(*self.TAX_LABEL).text
        # Example: 'Tax: $3.20'
        return float(text.split("$")[-1])

    def get_order_total(self):
        text = self.driver.find_element(*self.ORDER_TOTAL_LABEL).text
        # Example: 'Total: $43.18'
        return float(text.split("$")[-1])

    def get_summary_prices(self):
        item_total = self.get_element_text(self.ITEM_TOTAL)
        tax = self.get_element_text(self.TAX)
        total = self.get_element_text(self.TOTAL)
        return item_total, tax, total

    def get_summary_item_prices(self):
        price_elements = self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        return [float(e.text.replace("$", "").strip()) for e in price_elements]

    def click_finish(self):
        self.click(self.FINISH_BTN)

    def click_cancel(self):
        self.click(self.CANCEL_BTN)
