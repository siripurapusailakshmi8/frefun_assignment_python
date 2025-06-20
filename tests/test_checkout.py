import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.test_data import TestData

class TestCheckout:
    
    @pytest.fixture
    def setup_cart_with_items(self, authenticated_page):
        """Setup cart with items for checkout tests"""
        inventory_page = InventoryPage(authenticated_page)
        cart_page = CartPage(authenticated_page)
        
        # Add items to cart
        inventory_page.add_product_to_cart("sauce-labs-backpack")
        inventory_page.add_product_to_cart("sauce-labs-bike-light")
        
        # Go to cart and checkout
        inventory_page.click_shopping_cart()
        cart_page.click_checkout()
        
        return authenticated_page
    
    @pytest.mark.checkout
    def test_successful_checkout_process(self, setup_cart_with_items):
        """Test complete successful checkout process"""
        page = setup_cart_with_items
        checkout_page = CheckoutPage(page)
        
        # Step 1: Fill information
        checkout_page.fill_checkout_information(
            TestData.CHECKOUT_INFO["first_name"],
            TestData.CHECKOUT_INFO["last_name"],
            TestData.CHECKOUT_INFO["postal_code"]
        )
        checkout_page.click_continue()
        
        # Step 2: Verify overview and totals
        item_total = checkout_page.get_item_total()
        tax_amount = checkout_page.get_tax_amount()
        total_amount = checkout_page.get_total_amount()
        
        assert "Item total:" in item_total
        assert "Tax:" in tax_amount
        assert "Total:" in total_amount
        
        # Verify calculation
        item_value = float(item_total.split('$')[1])
        tax_value = float(tax_amount.split('$')[1])
        total_value = float(total_amount.split('$')[1])
        
        assert abs(total_value - (item_value + tax_value)) < 0.01
        
        # Step 3: Complete order
        checkout_page.click_finish()
        
        completion_message = checkout_page.get_completion_message()
        assert "thank you for your order" in completion_message.lower()
    
    @pytest.mark.checkout
    @pytest.mark.negative
    def test_checkout_with_empty_first_name(self, setup_cart_with_items):
        """Test checkout with empty first name"""
        page = setup_cart_with_items
        checkout_page = CheckoutPage(page)
        
        checkout_page.fill_checkout_information(
            "",
            TestData.CHECKOUT_INFO["last_name"],
            TestData.CHECKOUT_INFO["postal_code"]
        )
        checkout_page.click_continue()
        
        error_message = checkout_page.get_error_message()
        assert "first name is required" in error_message.lower()
    
    @pytest.mark.checkout
    @pytest.mark.negative
    def test_checkout_with_empty_last_name(self, setup_cart_with_items):
        """Test checkout with empty last name"""
        page = setup_cart_with_items
        checkout_page = CheckoutPage(page)
        
        checkout_page.fill_checkout_information(
            TestData.CHECKOUT_INFO["first_name"],
            "",
            TestData.CHECKOUT_INFO["postal_code"]
        )
        checkout_page.click_continue()
        
        error_message = checkout_page.get_error_message()
        assert "last name is required" in error_message.lower()
    
    @pytest.mark.checkout
    @pytest.mark.negative
    def test_checkout_with_empty_postal_code(self, setup_cart_with_items):
        """Test checkout with empty postal code"""
        page = setup_cart_with_items
        checkout_page = CheckoutPage(page)
        
        checkout_page.fill_checkout_information(
            TestData.CHECKOUT_INFO["first_name"],
            TestData.CHECKOUT_INFO["last_name"],
            ""
        )
        checkout_page.click_continue()
        
        error_message = checkout_page.get_error_message()
        assert "postal code is required" in error_message.lower()
    
    @pytest.mark.checkout
    def test_cancel_checkout_from_information_step(self, setup_cart_with_items):
        """Test canceling checkout from information step"""
        page = setup_cart_with_items
        checkout_page = CheckoutPage(page)
        cart_page = CartPage(page)
        
        checkout_page.click_cancel()
        
        # Should be back to cart page
        assert "cart.html" in page.url
        assert cart_page.get_cart_items_count() > 0
    
    @pytest.mark.checkout
    def test_cancel_checkout_from_overview_step(self, setup_cart_with_items):
        """Test canceling checkout from overview step"""
        page = setup_cart_with_items
        checkout_page = CheckoutPage(page)
        inventory_page = InventoryPage(page)
        
        # Complete first step
        checkout_page.fill_checkout_information(
            TestData.CHECKOUT_INFO["first_name"],
            TestData.CHECKOUT_INFO["last_name"],
            TestData.CHECKOUT_INFO["postal_code"]
        )
        checkout_page.click_continue()
        
        # Cancel from overview
        checkout_page.click_cancel()
        
        # Should be back to inventory page
        assert inventory_page.is_inventory_displayed()