from pathlib import Path
import pytest
import allure
from utilities.driver_factory import create_driver
from utilities.logger import get_logger

logger = get_logger()

@pytest.fixture
def driver():
    browser = create_driver()
    logger.info("Browser session started")
    yield browser
    browser.quit()
    logger.info("Browser session closed")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        browser = item.funcargs.get("driver")
        if browser:
            Path("screenshots").mkdir(exist_ok=True)
            screenshot_path = Path("screenshots") / f"{item.name}.png"
            browser.save_screenshot(str(screenshot_path))
            try:
                allure.attach(
                    browser.get_screenshot_as_png(),
                    name=f"{item.name}-failure",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                logger.exception("Could not attach failure screenshot")
            logger.error("Test failed. Screenshot saved to %s", screenshot_path)
