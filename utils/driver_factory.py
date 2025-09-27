import os
import tempfile
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

def get_driver(browser_name="chrome", incognito=False, headless=False):
    browser_name = browser_name.lower()
    remote_url = os.getenv("SELENIUM_REMOTE_URL")  # e.g. http://selenium:4444/wd/hub or http://selenium:4444

    if remote_url:
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            if incognito:
                options.add_argument("--incognito")
            if headless:
                options.add_argument("--headless=new")
            return webdriver.Remote(command_executor=remote_url, options=options)
        elif browser_name == "firefox":
            options = webdriver.FirefoxOptions()
            if incognito:
                options.add_argument("-private")
            if headless:
                options.add_argument("--headless")
            return webdriver.Remote(command_executor=remote_url, options=options)
        else:
            raise Exception(f"Unsupported browser: {browser_name}")

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()

        # Prefer Chromium in Docker if provided
        chrome_bin = os.getenv("CHROME_BIN")
        if chrome_bin:
            options.binary_location = chrome_bin

        if incognito:
            options.add_argument("--incognito")
        if headless:
            options.add_argument("--headless=new")

        # Harden for containers
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        # Use unique user data directory to avoid conflicts
        unique_user_data = f"/tmp/chrome-user-data-{uuid.uuid4().hex[:8]}"
        options.add_argument(f"--user-data-dir={unique_user_data}")

        # Use system chromedriver if present (Chromium image), else fallback to webdriver_manager
        system_chromedriver = os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")
        if os.path.exists(system_chromedriver):
            return webdriver.Chrome(service=ChromeService(system_chromedriver), options=options)

        path = ChromeDriverManager().install()
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
