from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import BASE_URL

class HomePage(BasePage):
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    SEARCH_INPUT = (By.ID, "small-searchterms")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "input.search-box-button")
    LOGOUT_LINK = (By.LINK_TEXT, "Log out")
    ACCOUNT_LINK = (By.CSS_SELECTOR, "a.account")

    def load(self):
        self.open(BASE_URL)

    def go_to_registration(self):
        self.click(self.REGISTER_LINK)

    def search(self, keyword):
        self.type_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)
        self.wait_url_contains("search")

    def is_logged_in(self):
        return bool(self.driver.find_elements(*self.LOGOUT_LINK))

    def logout(self):
        self.click(self.LOGOUT_LINK)
