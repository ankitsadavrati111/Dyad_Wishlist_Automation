import uuid
import pytest
import allure

from config.config import BASE_URL, PASSWORD, SEARCH_KEYWORD, INVALID_COUPON
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from pages.search_page import SearchPage
from pages.wishlist_page import WishlistPage
from pages.cart_page import CartPage
from utilities.logger import get_logger

logger = get_logger()

@allure.feature("Wishlist to Cart")
@allure.story("Complete shopping journey with invalid coupon")
def test_wishlist_to_cart_validation(driver):
    email = f"dyad.qa.{uuid.uuid4().hex[:10]}@example.com"
    logger.info("Starting scenario with generated email: %s", email)

    home = HomePage(driver)
    registration = RegistrationPage(driver)
    search = SearchPage(driver)
    wishlist = WishlistPage(driver)
    cart = CartPage(driver)

    with allure.step("Open website and register a unique user"):
        home.load()
        home.go_to_registration()
        registration.register_new_user(email)
        registration_message = registration.registration_success_message()
        assert "Your registration completed" in registration_message, (
            f"Registration did not succeed. Actual message: {registration_message}"
        )
        logger.info("Registration successful")
        registration.continue_after_registration()
        assert home.is_logged_in(), "User should be logged in after registration"

    with allure.step("Search for books and add two products to wishlist"):
        home.search(SEARCH_KEYWORD)
        selected_products = search.add_first_two_results_to_wishlist()
        assert len(selected_products) == 2
        assert selected_products[0] != selected_products[1], "Wishlist products must be different"
        logger.info("Selected wishlist products: %s", selected_products)

    with allure.step("Verify exactly two products are in wishlist"):
        wishlist.open_wishlist()
        wishlist_products = wishlist.product_names()
        assert len(wishlist_products) == 2, (
            f"Expected exactly 2 wishlist products, found {len(wishlist_products)}: {wishlist_products}"
        )
        for product in selected_products:
            assert product in wishlist_products, f"{product} was not found in wishlist"

    with allure.step("Move both wishlist products to shopping cart"):
        wishlist.move_all_to_cart()
        cart_products = cart.cart_product_names()
        assert len(cart_products) == 2, f"Expected 2 cart products, found {cart_products}"
        for product in selected_products:
            assert product in cart_products, f"{product} was not found in cart"

    with allure.step("Update quantity of one cart product to 2"):
        cart.set_first_product_quantity(2)
        quantities = [
            int(row.find_element(*cart.QUANTITY).get_attribute("value"))
            for row in cart.rows()
        ]
        assert quantities[0] == 2, f"Expected first product quantity 2, got {quantities[0]}"

    with allure.step("Verify cart subtotal using live unit prices and quantities"):
        expected = cart.expected_subtotal()
        actual = cart.displayed_subtotal()
        logger.info("Expected subtotal=%s, displayed subtotal=%s", expected, actual)
        assert actual == expected, (
            f"Subtotal mismatch: expected ${expected}, displayed ${actual}"
        )

    with allure.step("Apply invalid coupon and verify validation message"):
        coupon_message = cart.apply_invalid_coupon(INVALID_COUPON)
        assert coupon_message, "Expected an error message for an invalid coupon"
        assert "coupon" in coupon_message.lower(), (
            f"Unexpected invalid coupon message: {coupon_message}"
        )
        assert any(word in coupon_message.lower() for word in ("couldn't", "could not", "invalid", "not valid", "applied")), (
            f"Coupon message does not indicate rejection: {coupon_message}"
        )
        logger.info("Invalid coupon correctly rejected: %s", coupon_message)

    with allure.step("Logout and verify user is logged out"):
        cart.logout()
        assert not home.is_logged_in(), "Logout failed; Log out link is still visible"
        assert driver.find_elements(*home.REGISTER_LINK), "Register link should be visible after logout"
        logger.info("Logout successful")
