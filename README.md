# Dyad Technologies – Scenario 5: Wishlist to Cart Validation

Python + Selenium + Pytest + Page Object Model (POM) automation for:
https://demowebshop.tricentis.com/

## Scenario coverage

1. Register a new user using a generated unique email address.
2. Search using the keyword `Book`.
3. Add two different search results to Wishlist.
4. Assert that exactly two products are present in Wishlist.
5. Move both products to Shopping Cart and assert their presence.
6. Update the quantity of one product to 2.
7. Calculate expected subtotal from live unit prices × quantities and compare it with the displayed cart subtotal.
8. Apply an invalid coupon and assert that a rejection message is displayed.
9. Logout and assert that the logged-in navigation is no longer present.

The registration success, wishlist count, cart contents, subtotal, coupon rejection, and logout checks are implemented as assertions.

## Technology

- Python 3.10+
- Selenium WebDriver 4
- Pytest
- Allure Pytest adapter
- Page Object Model
- Python logging
- Selenium Manager (driver resolution)

## Prerequisites

- Python 3.10 or newer
- Google Chrome, Firefox, or Microsoft Edge installed
- Internet access to the demo website
- Allure command-line tool (optional, for rendering the HTML report)

## Setup (Windows PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the test

```powershell
pytest
```

Run with visible Chrome (default):

```powershell
$env:BROWSER="chrome"
$env:HEADLESS="false"
pytest
```

Run headless:

```powershell
$env:HEADLESS="true"
pytest
```

Use Firefox or Edge:

```powershell
$env:BROWSER="firefox"
pytest
```

Supported `BROWSER` values: `chrome`, `firefox`, `edge`.

Optional environment variables:

| Variable | Default | Purpose |
|---|---|---|
| `BASE_URL` | Demo Web Shop URL | Target environment |
| `BROWSER` | `chrome` | Browser selection |
| `HEADLESS` | `false` | Headless execution |
| `WAIT_TIMEOUT` | `15` | Explicit wait timeout in seconds |
| `TEST_PASSWORD` | `Test@12345` | Password for generated test account |

## Allure report

```powershell
pytest --alluredir=allure-results
allure serve allure-results
```

The test also writes execution logs to `logs/automation.log` and failure screenshots to `screenshots/`.

## Framework design

- `pages/`: page-specific locators and UI actions. Tests do not contain page locators.
- `utilities/driver_factory.py`: browser creation and browser options.
- `utilities/logger.py`: shared structured timestamped logging.
- `config/config.py`: environment-driven settings and test constants.
- `conftest.py`: WebDriver lifecycle fixture and failure screenshot hook.
- `tests/`: business workflow and assertions.

## Dynamic data and calculation

- Email is generated for each run with UUID to avoid duplicate-account conflicts.
- Product titles are read from the live search results and checked again in Wishlist and Cart.
- Unit prices and quantities are read from the cart at runtime.
- Expected subtotal = sum of each cart line's unit price × quantity. `Decimal` is used instead of binary floating-point to avoid currency rounding errors.


