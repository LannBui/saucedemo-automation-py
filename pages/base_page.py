from tkinter.tix import Select

from select import select
from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def enter_text(self, locator, value):
        self.wait.until(EC.visibility_of_element_located(locator)).clear()
        self.driver.find_element(*locator).send_keys(value)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def get_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def is_element_visible(self, locator):
        elements = self.find_elements(locator)
        return any(e.is_displayed() for e in elements)

    def select_by_visible_text(self, locator, text):
        element = self.driver.find_element(*locator)
        dropdown = Select(element)
        dropdown.select_by_visible_text(text)

    def get_element_text(self, locator):
        return self.driver.find_element(*locator).text.strip()
