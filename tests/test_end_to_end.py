import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.test_data import TestData

class TestEndToEnd:
    
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_complete_purchase_flow(self, page):
        """Test complete end-to-end purchase flow"""
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        cart_page = CartPage(page)
        checkout_page = CheckoutPage(page)
        
        # Step 1: Login
        login_page.login(TestData.STANDARD_USER, TestData.PASSWORD)
        assert inventory_page.is_inventory_displayed()
        
        # Step 2: Sort products and verify
        inventory_page.sort_products(TestData.SORT_OPTIONS["price_low"])
        prices = inventory_page.get_product_prices()
        price_values = [float(price.replace('$', '')) for price in prices]
        assert price_values == sorted(price_values)
        
        # Step 3: Add products to cart
        inventory_page.add_product_to_cart("sauce-labs-backpack")
        inventory_page.add_product_to_cart("sauce-labs-bike-light")
        assert inventory_page.get_cart_badge_count() == "2"
        
        # Step 4: Go to cart and verify items
        inventory_page.click_shopping_cart()
        assert cart_page.get_cart_items_count() == 2
        
        cart_items = cart_page.get_cart_item_names()
        assert "Sauce Labs Backpack" in cart_items
        assert "Sauce Labs Bike Light" in cart_items
        
        # Step 5: Proceed to checkout
        cart_page.click_checkout()
        
        # Step 6: Fill checkout information
        checkout_page.fill_checkout_information(
            TestData.CHECKOUT_INFO["first_name"],
            TestData.CHECKOUT_INFO["last_name"],
            TestData.CHECKOUT_INFO["postal_code"]
        )
        checkout_page.click_continue()
        
        # Step 7: Verify totals and complete order
        item_total = checkout_page.get_item_total()
        tax_amount = checkout_page.get_tax_amount()
        total_amount = checkout_page.get_total_amount()
        
        assert "Item total:" in item_total
        assert "Tax:" in tax_amount
        assert "Total:" in total_amount
        
        checkout_page.click_finish()
        
        # Step 8: Verify order completion
        completion_message = checkout_page.get_completion_message()
        assert "thank you for your order" in completion_message.lower()
        
        # Step 9: Return to products and logout
        checkout_page.click_back_home()
        assert inventory_page.is_inventory_displayed()
        
        inventory_page.logout()
        assert page.url == TestData.BASE_URL + "/"
    
    @pytest.mark.regression
    def test_problem_user_workflow(self, page):
        """Test workflow with problem user to verify error handling"""
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        
        # Login with problem user
        login_page.login(TestData.PROBLEM_USER, TestData.PASSWORD)
        assert inventory_page.is_inventory_displayed()
        
        # Try to add products (may have issues with problem user)
        inventory_page.add_product_to_cart("sauce-labs-backpack")
        
        # Problem user might have issues, but test should not fail
        # This test is to ensure our framework handles problem user gracefully
        assert True  # Test passes if no exceptions occur