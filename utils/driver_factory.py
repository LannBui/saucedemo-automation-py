import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

def get_driver(browser_name="chrome", incognito=False, headless=False):
    browser_name = browser_name.lower()
    if browser_name == "chrome":
        path = ChromeDriverManager().install()
        options = webdriver.ChromeOptions()
        if incognito:
            options.add_argument("--incognito")
        if headless:
            options.add_argument("--headless")
        return webdriver.Chrome(service=ChromeService(path), options=options)
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        if incognito:
            options.add_argument("-private")
        if headless:
            options.add_argument("--headless")
        return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    else:
        raise Exception(f"Unsupported browser: {browser_name}")
