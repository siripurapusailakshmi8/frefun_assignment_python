from playwright.sync_api import Page
from abc import ABC

class BasePage(ABC):
    def __init__(self, page: Page):
        self.page = page
    
    def wait_for_page_load(self, timeout: int = 30000):
        """Wait for page to be fully loaded"""
        self.page.wait_for_load_state("networkidle", timeout=timeout)
    
    def get_page_title(self) -> str:
        """Get current page title"""
        return self.page.title()
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.page.url
    
    def click_element(self, selector: str):
        """Click element with wait"""
        self.page.wait_for_selector(selector, state="visible")
        self.page.click(selector)
    
    def fill_text(self, selector: str, text: str):
        """Fill text in input field"""
        self.page.wait_for_selector(selector, state="visible")
        self.page.fill(selector, text)
    
    def get_text(self, selector: str) -> str:
        """Get text from element"""
        self.page.wait_for_selector(selector, state="visible")
        return self.page.inner_text(selector)
    
    def is_element_visible(self, selector: str) -> bool:
        """Check if element is visible"""
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=5000)
            return True
        except:
            return False