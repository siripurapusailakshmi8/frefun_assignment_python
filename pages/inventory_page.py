from pages.base_page import BasePage
from playwright.sync_api import Page
from typing import List

class InventoryPage(BasePage):
    # Locators
    INVENTORY_CONTAINER = ".inventory_container"
    INVENTORY_ITEMS = ".inventory_item"
    INVENTORY_ITEM_NAME = ".inventory_item_name"
    INVENTORY_ITEM_PRICE = ".inventory_item_price"
    ADD_TO_CART_BUTTON = "button[data-test^='add-to-cart']"
    REMOVE_FROM_CART_BUTTON = "button[data-test^='remove']"
    SHOPPING_CART_BADGE = ".shopping_cart_badge"
    SHOPPING_CART_LINK = ".shopping_cart_link"
    SORT_DROPDOWN = "[data-test='product_sort_container']"
    HAMBURGER_MENU = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"
   
    def __init__(self, page: Page):
        super().__init__(page)
   
    def is_inventory_displayed(self) -> bool:
        """Check if inventory page is displayed"""
        return self.is_element_visible(self.INVENTORY_CONTAINER)
   
    def get_product_names(self) -> List[str]:
        """Get all product names"""
        self.page.wait_for_selector(self.INVENTORY_ITEM_NAME)
        return self.page.locator(self.INVENTORY_ITEM_NAME).all_inner_texts()
   
    def get_product_prices(self) -> List[str]:
        """Get all product prices"""
        self.page.wait_for_selector(self.INVENTORY_ITEM_PRICE)
        return self.page.locator(self.INVENTORY_ITEM_PRICE).all_inner_texts()
   
    def sort_products(self, sort_option: str):
        """Sort products by given option"""
        try:
            # Wait for dropdown to be visible and ready
            self.page.wait_for_selector(self.SORT_DROPDOWN, state="visible", timeout=15000)
            
            # Additional wait to ensure dropdown is fully interactive
            self.page.wait_for_timeout(2000)
            
            # Use value attribute explicitly
            self.page.select_option(self.SORT_DROPDOWN, value=sort_option)
            
            # Wait for sorting animation/network to complete
            self.page.wait_for_timeout(3000)
            
        except Exception as e:
            print(f"Primary sort method failed: {e}")
            # Fallback method
            try:
                # Click approach
                self.page.click(self.SORT_DROPDOWN)
                self.page.wait_for_timeout(1000)
                
                # Try to click the specific option
                option_selector = f"option[value='{sort_option}']"
                self.page.click(option_selector)
                self.page.wait_for_timeout(3000)
                
            except Exception as fallback_error:
                print(f"Fallback method failed: {fallback_error}")
                # Final fallback - use JavaScript
                self.page.evaluate(f"""
                    const dropdown = document.querySelector('[data-test="product_sort_container"]');
                    if (dropdown) {{
                        dropdown.value = '{sort_option}';
                        dropdown.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }}
                """)
                self.page.wait_for_timeout(3000)
   
    def sort_products_alternative(self, sort_option: str):
        """Alternative sorting method if the main one fails"""
        try:
            # Click approach for dropdowns that don't work with select_option
            self.page.click(self.SORT_DROPDOWN)
            self.page.wait_for_timeout(500)
           
            # Select the option by value
            option_selector = f"{self.SORT_DROPDOWN} option[value='{sort_option}']"
            self.page.click(option_selector)
           
            # Wait for sorting to complete
            self.page.wait_for_timeout(2000)
           
        except Exception as e:
            print(f"Alternative sorting method failed: {e}")
            raise
   
    def add_product_to_cart(self, product_name: str):
        """Add specific product to cart"""
        try:
            product_button = f"button[data-test='add-to-cart-{product_name.lower().replace(' ', '-')}']"
            self.page.wait_for_selector(product_button, state="visible", timeout=5000)
            self.click_element(product_button)
            # Wait a moment for the cart to update
            self.page.wait_for_timeout(500)
        except Exception as e:
            print(f"Error adding product {product_name} to cart: {e}")
            raise
   
    def remove_product_from_cart(self, product_name: str):
        """Remove specific product from cart"""
        try:
            product_button = f"button[data-test='remove-{product_name.lower().replace(' ', '-')}']"
            self.page.wait_for_selector(product_button, state="visible", timeout=5000)
            self.click_element(product_button)
            # Wait a moment for the cart to update
            self.page.wait_for_timeout(500)
        except Exception as e:
            print(f"Error removing product {product_name} from cart: {e}")
            raise
   
    def get_cart_badge_count(self) -> str:
        """Get shopping cart badge count"""
        try:
            if self.is_element_visible(self.SHOPPING_CART_BADGE):
                return self.get_text(self.SHOPPING_CART_BADGE)
            return "0"
        except Exception:
            return "0"
   
    def click_shopping_cart(self):
        """Click shopping cart icon"""
        self.click_element(self.SHOPPING_CART_LINK)
   
    def logout(self):
        """Logout from application"""
        try:
            # Click hamburger menu
            self.click_element(self.HAMBURGER_MENU)
           
            # Wait for sidebar to appear
            self.page.wait_for_selector(self.LOGOUT_LINK, state="visible", timeout=5000)
           
            # Click logout
            self.click_element(self.LOGOUT_LINK)
           
            # Wait for logout to complete
            self.page.wait_for_timeout(1000)
           
        except Exception as e:
            print(f"Error during logout: {e}")
            raise