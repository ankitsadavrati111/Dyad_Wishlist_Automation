import os

BASE_URL = os.getenv("BASE_URL", "https://demowebshop.tricentis.com")
BROWSER = os.getenv("BROWSER", "chrome").lower()
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
WAIT_TIMEOUT = int(os.getenv("WAIT_TIMEOUT", "15"))
PASSWORD = os.getenv("TEST_PASSWORD", "Test@12345")
FIRST_NAME = os.getenv("TEST_FIRST_NAME", "Automation")
LAST_NAME = os.getenv("TEST_LAST_NAME", "Candidate")
SEARCH_KEYWORD = "Book"
INVALID_COUPON = "INVALID-DYAD-2026"
