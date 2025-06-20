import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from utils.test_data import TestData

@pytest.fixture(scope="session")
def browser():
    """Create browser instance for the session"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=1000,  
            timeout=60000  
        )
        yield browser
        browser.close()

@pytest.fixture(scope="function")  
def page(context: BrowserContext):
    """Create new page for each test"""
    page = context.new_page()
    page.set_default_timeout(60000)  # Increase default timeout
    page.goto(TestData.BASE_URL)
    yield page
    page.close()

@pytest.fixture(scope="function")
def context(browser: Browser):
    """Create new browser context for each test"""
    context = browser.new_context(
        viewport={'width': 1280, 'height': 720},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def authenticated_page(page: Page):
    """Login and return authenticated page"""
    from pages.login_page import LoginPage
    login_page = LoginPage(page)
    login_page.login(TestData.STANDARD_USER, TestData.PASSWORD)
    yield page
