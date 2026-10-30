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

## Assumptions and limitations

- The assessment asks for two books but does not prescribe exact titles. The test selects the first two products returned by the `Book` search and verifies that the same products travel through the workflow.
- The test uses the site's visible registration and shopping workflow; it does not place an order or enter payment information.
- The demo site's markup, availability, and anti-bot/rate-limiting behavior can change. If a locator changes, update the relevant Page Object rather than putting selectors into the test.
- The test account uses synthetic data and should not contain real personal information.
- The coupon assertion checks that the site displays a coupon-related rejection message; exact wording may change on the demo site.
- Run the test against the public demo environment and confirm it passes in your own browser before submitting. This generated project has not been executed against the live site in this environment.

## Suggested Git commit history

```bash
git init
git add requirements.txt pytest.ini .gitignore README.md config/
git commit -m "Initialize Python Selenium pytest framework"

git add utilities/
git commit -m "Add browser factory and logging utilities"

git add pages/
git commit -m "Implement page objects for registration wishlist and cart"

git add conftest.py tests/
git commit -m "Automate wishlist to cart end-to-end scenario"

git add README.md
git commit -m "Document setup execution and scenario assumptions"
```

## Before sharing with the interviewer

1. Create the virtual environment and install dependencies.
2. Run `pytest` and resolve any live-site locator or behavior differences.
3. Inspect the generated screenshot/log if the test fails.
4. Generate the Allure report.
5. Commit incrementally and push the repository to GitHub.
6. Be prepared to explain every page object, wait, assertion, and subtotal calculation.
