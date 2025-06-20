from pages.base_page import BasePage
from playwright.sync_api import Page
from typing import List

class CartPage(BasePage):
    # Locators
    CART_ITEMS = ".cart_item"
    CART_ITEM_NAME = ".inventory_item_name"
    CART_ITEM_PRICE = ".inventory_item_price"
    CONTINUE_SHOPPING_BUTTON = "[data-test='continue-shopping']"
    CHECKOUT_BUTTON = "[data-test='checkout']"
    REMOVE_BUTTON = "button[data-test^='remove']"
    CART_QUANTITY = ".cart_quantity"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def get_cart_items_count(self) -> int:
        """Get number of items in cart"""
        return len(self.page.locator(self.CART_ITEMS).all())
    
    def get_cart_item_names(self) -> List[str]:
        """Get names of items in cart"""
        if self.get_cart_items_count() > 0:
            return self.page.locator(self.CART_ITEM_NAME).all_inner_texts()
        return []
    
    def get_cart_item_prices(self) -> List[str]:
        """Get prices of items in cart"""
        if self.get_cart_items_count() > 0:
            return self.page.locator(self.CART_ITEM_PRICE).all_inner_texts()
        return []
    
    def click_continue_shopping(self):
        """Click continue shopping button"""
        self.click_element(self.CONTINUE_SHOPPING_BUTTON)
    
    def click_checkout(self):
        """Click checkout button"""
        self.click_element(self.CHECKOUT_BUTTON)
    
    def remove_item_from_cart(self, index: int = 0):
        """Remove item from cart by index"""
        remove_buttons = self.page.locator(self.REMOVE_BUTTON).all()
        if index < len(remove_buttons):
            remove_buttons[index].click()