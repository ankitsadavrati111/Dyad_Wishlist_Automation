from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import BASE_URL, FIRST_NAME, LAST_NAME, PASSWORD

class RegistrationPage(BasePage):
    GENDER_MALE = (By.ID, "gender-male")
    FIRST_NAME = (By.ID, "FirstName")
    LAST_NAME = (By.ID, "LastName")
    EMAIL = (By.ID, "Email")
    PASSWORD = (By.ID, "Password")
    CONFIRM_PASSWORD = (By.ID, "ConfirmPassword")
    REGISTER_BUTTON = (By.ID, "register-button")
    RESULT = (By.CSS_SELECTOR, ".result")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, ".register-continue-button")

    def register_new_user(self, email):
        self.click(self.GENDER_MALE)
        self.type_text(self.FIRST_NAME, FIRST_NAME)
        self.type_text(self.LAST_NAME, LAST_NAME)
        self.type_text(self.EMAIL, email)
        self.type_text(self.PASSWORD, PASSWORD)
        self.type_text(self.CONFIRM_PASSWORD, PASSWORD)
        self.click(self.REGISTER_BUTTON)

    def registration_success_message(self):
        return self.get_text(self.RESULT)

    def continue_after_registration(self):
        self.click(self.CONTINUE_BUTTON)
