
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from config.config import BASE_URL


class SearchPage(BasePage):

    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".product-item")
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".product-title a")

    ADD_TO_WISHLIST = (
        By.CSS_SELECTOR,
        "input.add-to-wishlist-button"
    )

    NOTIFICATION = (
        By.CSS_SELECTOR,
        ".bar-notification"
    )

    def add_first_two_results_to_wishlist(self):

        # Step 1: Check products returned by Book search
        self.wait.until(
            EC.presence_of_all_elements_located(
                self.PRODUCT_ITEMS
            )
        )

        items = self.driver.find_elements(
            *self.PRODUCT_ITEMS
        )

        print("Products found in search:", len(items))

        # Step 2: Fallback to Books category if needed
        if len(items) < 2:

            print(
                "Less than 2 search results. "
                "Opening Books category."
            )

            self.open(f"{BASE_URL}/books")

            self.wait.until(
                EC.presence_of_all_elements_located(
                    self.PRODUCT_ITEMS
                )
            )

            items = self.driver.find_elements(
                *self.PRODUCT_ITEMS
            )

        # Step 3: Validate availability
        assert len(items) >= 2, (
            f"Expected at least 2 books, "
            f"but found {len(items)}"
        )

        selected_products = []

        # Step 4: Open first two product details
        for index in range(2):

            items = self.driver.find_elements(
                *self.PRODUCT_ITEMS
            )

            product = items[index]

            product_name = product.find_element(
                *self.PRODUCT_TITLE
            ).text.strip()

            selected_products.append(product_name)

            print(
                f"Opening product {index + 1}: "
                f"{product_name}"
            )

            product.find_element(
                *self.PRODUCT_TITLE
            ).click()

            # Step 5: Add product to wishlist
            self.click(self.ADD_TO_WISHLIST)

            self.wait.until(
                EC.visibility_of_element_located(
                    self.NOTIFICATION
                )
            )

            print(
                f"Added to wishlist: {product_name}"
            )

            # Step 6: Return to Books category
            self.driver.back()

            self.wait.until(
                EC.presence_of_all_elements_located(
                    self.PRODUCT_ITEMS
                )
            )

        return selected_products
