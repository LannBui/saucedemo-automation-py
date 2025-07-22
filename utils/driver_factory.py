from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

def get_driver(browser_name="chrome"):
    if browser_name == "chrome":
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif browser_name == "firefox":
        return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    else:
        raise Exception(f"Unsupported browser: {browser_name}")
