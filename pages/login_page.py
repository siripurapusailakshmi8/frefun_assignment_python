from pages.base_page import BasePage
from playwright.sync_api import Page

class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = "[data-test='username']"
    PASSWORD_INPUT = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-button']"
    ERROR_MESSAGE = "[data-test='error']"
    ERROR_CLOSE_BUTTON = ".error-button"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def enter_username(self, username: str):
        """Enter username"""
        self.fill_text(self.USERNAME_INPUT, username)
    
    def enter_password(self, password: str):
        """Enter password"""
        self.fill_text(self.PASSWORD_INPUT, password)
    
    def click_login(self):
        """Click login button"""
        self.click_element(self.LOGIN_BUTTON)
    
    def login(self, username: str, password: str):
        """Complete login process"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
    
    def get_error_message(self) -> str:
        """Get error message text"""
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_displayed(self) -> bool:
        """Check if error message is displayed"""
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def close_error_message(self):
        """Close error message"""
        self.click_element(self.ERROR_CLOSE_BUTTON)