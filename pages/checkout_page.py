from pages.base_page import BasePage
from playwright.sync_api import Page

class CheckoutPage(BasePage):
    # Step 1 - Information
    FIRST_NAME_INPUT = "[data-test='firstName']"
    LAST_NAME_INPUT = "[data-test='lastName']"
    POSTAL_CODE_INPUT = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"
    ERROR_MESSAGE = "[data-test='error']"
    
    # Step 2 - Overview
    ITEM_TOTAL = ".summary_subtotal_label"
    TAX_TOTAL = ".summary_tax_label"
    TOTAL_AMOUNT = ".summary_total_label"
    FINISH_BUTTON = "[data-test='finish']"
    CANCEL_BUTTON = "[data-test='cancel']"
    
    # Step 3 - Complete
    COMPLETE_HEADER = ".complete-header"
    BACK_HOME_BUTTON = "[data-test='back-to-products']"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    # Step 1 Methods
    def fill_checkout_information(self, first_name: str, last_name: str, postal_code: str):
        """Fill checkout information"""
        self.fill_text(self.FIRST_NAME_INPUT, first_name)
        self.fill_text(self.LAST_NAME_INPUT, last_name) 
        self.fill_text(self.POSTAL_CODE_INPUT, postal_code)
    
    def click_continue(self):
        """Click continue button"""
        self.click_element(self.CONTINUE_BUTTON)
    
    def get_error_message(self) -> str:
        """Get error message"""
        return self.get_text(self.ERROR_MESSAGE)
    
    # Step 2 Methods
    def get_item_total(self) -> str:
        """Get item total amount"""
        return self.get_text(self.ITEM_TOTAL)
    
    def get_tax_amount(self) -> str:
        """Get tax amount"""
        return self.get_text(self.TAX_TOTAL)
    
    def get_total_amount(self) -> str:
        """Get final total amount"""
        return self.get_text(self.TOTAL_AMOUNT)
    
    def click_finish(self):
        """Click finish button"""
        self.click_element(self.FINISH_BUTTON)
    
    def click_cancel(self):
        """Click cancel button"""
        self.click_element(self.CANCEL_BUTTON)
    
    # Step 3 Methods
    def get_completion_message(self) -> str:
        """Get order completion message"""
        return self.get_text(self.COMPLETE_HEADER)
    
    def click_back_home(self):
        """Click back to products button"""
        self.click_element(self.BACK_HOME_BUTTON)