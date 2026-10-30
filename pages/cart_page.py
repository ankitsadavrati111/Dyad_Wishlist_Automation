from decimal import Decimal, InvalidOperation
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class CartPage(BasePage):
    CART_ROWS = (By.CSS_SELECTOR, "tr.cart-item-row")
    PRODUCT_NAME = (By.CSS_SELECTOR, ".product a")
    UNIT_PRICE = (By.CSS_SELECTOR, ".product-unit-price")
    QUANTITY = (By.CSS_SELECTOR, "input.qty-input")
    LINE_SUBTOTAL = (By.CSS_SELECTOR, ".product-subtotal")
    UPDATE_CART = (By.NAME, "updatecart")
    SUBTOTAL = (By.CSS_SELECTOR, ".order-subtotal .cart-total-right .value-summary")
    COUPON_INPUT = (By.ID, "discountcouponcode")
    APPLY_COUPON = (By.NAME, "applydiscountcouponcode")
    COUPON_ERROR = (By.CSS_SELECTOR, ".coupon-box .message, .message-error")
    LOGOUT_LINK = (By.LINK_TEXT, "Log out")

    def wait_for_cart(self):
        self.wait.until(EC.presence_of_all_elements_located(self.CART_ROWS))

    def rows(self):
        self.wait_for_cart()
        return self.driver.find_elements(*self.CART_ROWS)

    def cart_product_names(self):
        names = []
        for row in self.rows():
            names.append(row.find_element(*self.PRODUCT_NAME).text.strip())
        return names

    @staticmethod
    def money(value):
        cleaned = value.replace("$", "").replace(",", "").strip()
        return Decimal(cleaned)

    def set_first_product_quantity(self, quantity):
        rows = self.rows()
        if not rows:
            raise AssertionError("Shopping cart is empty")
        qty = rows[0].find_element(*self.QUANTITY)
        qty.clear()
        qty.send_keys(str(quantity))
        self.click(self.UPDATE_CART)
        # Updating the cart can refresh the table; always locate the row again.
        self.wait.until(
            lambda d: d.find_element(*self.CART_ROWS).find_element(
                *self.QUANTITY
            ).get_attribute("value") == str(quantity)
        )

    def expected_subtotal(self):
        expected = Decimal("0.00")
        for row in self.rows():
            unit_price = self.money(row.find_element(*self.UNIT_PRICE).text)
            quantity = int(row.find_element(*self.QUANTITY).get_attribute("value"))
            expected += unit_price * quantity
        return expected.quantize(Decimal("0.01"))

    def displayed_subtotal(self):
        return self.money(self.get_text(self.SUBTOTAL)).quantize(Decimal("0.01"))

    def apply_invalid_coupon(self, code):
        self.type_text(self.COUPON_INPUT, code)
        self.click(self.APPLY_COUPON)
        return self.get_text(self.COUPON_ERROR)

    def logout(self):
        self.click(self.LOGOUT_LINK)
