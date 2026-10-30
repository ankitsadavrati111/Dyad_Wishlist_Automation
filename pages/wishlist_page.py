from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class WishlistPage(BasePage):
    WISHLIST_LINK = (By.LINK_TEXT, "Wishlist")
    WISHLIST_ROWS = (By.CSS_SELECTOR, "table.wishlist-content tr")
    ADD_TO_CART_CHECKBOXES = (By.CSS_SELECTOR, "input[name='addtocart']")
    ADD_SELECTED_TO_CART = (By.NAME, "addtocartbutton")
    PRODUCT_NAMES = (By.CSS_SELECTOR, "table.wishlist-content .product")

    def open_wishlist(self):
        self.click(self.WISHLIST_LINK)
        self.wait_url_contains("wishlist")

    def product_names(self):
        rows = self.driver.find_elements(*self.WISHLIST_ROWS)
        names = []
        for row in rows:
            links = row.find_elements(By.CSS_SELECTOR, ".product a")
            if links:
                names.append(links[0].text.strip())
        return names

    def move_all_to_cart(self):
        checkboxes = self.wait.until(
            EC.presence_of_all_elements_located(self.ADD_TO_CART_CHECKBOXES)
        )
        if len(checkboxes) < 2:
            raise AssertionError(f"Expected 2 wishlist selection checkboxes, found {len(checkboxes)}")
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                self.driver.execute_script("arguments[0].click();", checkbox)
        self.click(self.ADD_SELECTED_TO_CART)
        self.wait_url_contains("cart")
