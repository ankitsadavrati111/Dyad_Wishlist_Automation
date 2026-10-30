
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from config.config import BROWSER, HEADLESS


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def create_driver():

    if BROWSER == "chrome":

        options = ChromeOptions()

        if HEADLESS:
            options.add_argument("--headless=new")

        options.add_argument("--window-size=1440,1000")
        options.add_argument("--disable-notifications")

        # Use manually downloaded ChromeDriver
        driver_path = PROJECT_ROOT / "drivers" / "chromedriver.exe"

        if not driver_path.is_file():
            raise FileNotFoundError(
                f"ChromeDriver not found at: {driver_path}"
            )

        service = ChromeService(
            executable_path=str(driver_path)
        )

        driver = webdriver.Chrome(
            service=service,
            options=options
        )

    elif BROWSER == "firefox":

        options = FirefoxOptions()

        if HEADLESS:
            options.add_argument("-headless")

        driver = webdriver.Firefox(options=options)
        driver.set_window_size(1440, 1000)

    elif BROWSER == "edge":

        options = EdgeOptions()

        if HEADLESS:
            options.add_argument("--headless=new")

        driver = webdriver.Edge(options=options)
        driver.set_window_size(1440, 1000)

    else:
        raise ValueError(f"Unsupported browser: {BROWSER}")

    driver.implicitly_wait(0)

    return driver
