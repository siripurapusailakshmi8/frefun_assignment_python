# SauceDemo Test Framework

A robust test automation framework for validating the SauceDemo e-commerce website using Playwright and Pytest.

---

## Features

- Page Object Model (POM) – Organized, reusable test structure  
- Comprehensive Coverage – Login, inventory, cart, checkout, end-to-end scenarios  
- Test Types – Smoke, regression, negative, and edge case coverage  
- Parallel Execution – Using `pytest-xdist`  
- HTML Reporting – Clear test reports using `pytest-html`  
- Data-Driven Testing – Centralized test data  
- Cross-Browser Support – Easily configurable via `conftest.py`

---

## Test Coverage

### Mandatory Tests

- **Login**: Valid/invalid credentials, locked-out users, empty fields  
- **Product Sorting**: Name (A-Z, Z-A), Price (Low-High, High-Low)  
- **Product Display**: Product visibility, name, price, image  
- **Cart Management**: Add/remove items, cart badge updates  
- **Payment Totals**: Subtotal, tax, final total validation  
- **Checkout**: Valid flow, form validation, error handling  
- **Logout**: Proper session termination  
- **Edge/Negative Cases**: Form validations, incorrect input handling

### Bonus Features

- HTML Reports via `pytest-html`  
- Parallel Testing via `pytest-xdist`  
- Comprehensive Documentation included

---

## Setup & Installation

### Prerequisites

- Python 3.8+
- pip package manager


---

## Assumptions

- The locators of the site will remain same at the time of execution.
- The SauceDemo website is accessible at [https://www.saucedemo.com](https://www.saucedemo.com)
- Valid test user credentials are available:
  - Username: `standard_user`
  - Password: `secret_sauce`
- A stable internet connection is available during test execution
- The testing environment supports the Chromium browser
- The default network timeout of 30 seconds is sufficient for most actions

---

## Constraints

- The framework is designed specifically for the current structure of the SauceDemo website
- By default, tests are configured to run only on the **Chromium** browser
  - This can be modified in `conftest.py` to support Firefox or WebKit
- Some tests include artificial delays (e.g., `time.sleep()`) to demonstrate behavior
- Only functional UI test scenarios are covered—non-functional testing (e.g., performance, accessibility) is out of scope

---

## Known Limitations

- Sorting functionality tests may fail or timeout on slow systems (timeouts can be increased in `conftest.py`)
- Tests are executed in **headed mode** by default, which is slower; to improve performance, set headless mode in `conftest.py`
- Parallel test execution using `pytest-xdist` is limited by the SauceDemo website’s performance and rate-limiting
- Cross-browser support is not included out-of-the-box and requires configuration
- Data used in tests is static and not fetched from external sources or databases

---
## Installation Steps

```bash
# 1. Clone the repository
git clone <repo-url>
cd saucedemo_tests

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Playwright and browser binaries
playwright install chromium


### Verify Installation

pytest tests/test_login.py::TestLogin::test_successful_login_standard_user -v

### Running Tests

### Basic Commands

# Run all tests
pytest

# With verbose output
pytest -v

# Run specific test file
pytest tests/test_login.py

# Run by test marker
pytest -m smoke       # Smoke tests
pytest -m regression  # Regression tests
pytest -m negative    # Negative test cases


### Generate HTML Reports

# Basic HTML report
pytest --html=reports/report.html --self-contained-html

# With parallel execution
pytest -n 4 --html=reports/report.html --self-contained-html


