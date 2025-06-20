import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.test_data import TestData

class TestCart:
    
    @pytest.mark.cart
    def test_view_cart_with_items(self, authenticated_page):
        """Test viewing cart with items"""
        inventory_page = InventoryPage(authenticated_page)
        cart_page = CartPage(authenticated_page)
        
        # Add items to cart
        inventory_page.add_product_to_cart("sauce-labs-backpack")
        inventory_page.add_product_to_cart("sauce-labs-bike-light")
        
        # Navigate to cart
        inventory_page.click_shopping_cart()
        
        # Verify cart contents
        assert cart_page.get_cart_items_count() == 2
        cart_items = cart_page.get_cart_item_names()
        assert "Sauce Labs Backpack" in cart_items
        assert "Sauce Labs Bike Light" in cart_items
    
    @pytest.mark.cart
    def test_remove_item_from_cart_page(self, authenticated_page):
        """Test removing item from cart page"""
        inventory_page = InventoryPage(authenticated_page)
        cart_page = CartPage(authenticated_page)
        
        # Add item and go to cart
        inventory_page.add_product_to_cart("sauce-labs-backpack")
        inventory_page.click_shopping_cart()
        
        assert cart_page.get_cart_items_count() == 1
        
        # Remove item from cart
        cart_page.remove_item_from_cart(0)
        
        assert cart_page.get_cart_items_count() == 0
    
    @pytest.mark.cart
    def test_continue_shopping_from_cart(self, authenticated_page):
        """Test continue shopping functionality"""
        inventory_page = InventoryPage(authenticated_page)
        cart_page = CartPage(authenticated_page)
        
        # Add item and go to cart
        inventory_page.add_product_to_cart("sauce-labs-backpack")
        inventory_page.click_shopping_cart()
        
        # Continue shopping
        cart_page.click_continue_shopping()
        
        # Should be back to inventory page
        assert inventory_page.is_inventory_displayed()
        assert "inventory.html" in authenticated_page.url
    
    @pytest.mark.cart
    def test_cart_price_calculation(self, authenticated_page):
        """Test cart displays correct prices"""
        inventory_page = InventoryPage(authenticated_page)
        cart_page = CartPage(authenticated_page)
        
        # Get price from inventory page
        inventory_page.add_product_to_cart("sauce-labs-backpack")
        inventory_prices = inventory_page.get_product_prices()
        backpack_price = None
        
        for i, name in enumerate(inventory_page.get_product_names()):
            if "Backpack" in name:
                backpack_price = inventory_prices[i]
                break
        
        # Go to cart and verify price
        inventory_page.click_shopping_cart()
        cart_prices = cart_page.get_cart_item_prices()
        
        assert backpack_price in cart_prices