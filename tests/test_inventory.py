import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.test_data import TestData

class TestInventory:
    
    @pytest.mark.regression
    def test_products_are_displayed(self, authenticated_page):
        """Test that products are displayed on inventory page"""
        inventory_page = InventoryPage(authenticated_page)
        
        assert inventory_page.is_inventory_displayed()
        
        product_names = inventory_page.get_product_names()
        assert len(product_names) > 0
        
        product_prices = inventory_page.get_product_prices()
        assert len(product_prices) > 0
        assert len(product_names) == len(product_prices)
    
    @pytest.mark.regression
    def test_sort_products_by_name_ascending(self, authenticated_page):
        """Test sorting products by name A-Z"""
        inventory_page = InventoryPage(authenticated_page)
        
        inventory_page.sort_products(TestData.SORT_OPTIONS["name_asc"])
        product_names = inventory_page.get_product_names()
        
        # Verify products are sorted alphabetically
        assert product_names == sorted(product_names)
    
    @pytest.mark.regression  
    def test_sort_products_by_name_descending(self, authenticated_page):
        """Test sorting products by name Z-A"""
        inventory_page = InventoryPage(authenticated_page)
        
        inventory_page.sort_products(TestData.SORT_OPTIONS["name_desc"])
        product_names = inventory_page.get_product_names()
        
        # Verify products are sorted reverse alphabetically
        assert product_names == sorted(product_names, reverse=True)
    
    @pytest.mark.regression
    def test_sort_products_by_price_low_to_high(self, authenticated_page):
        """Test sorting products by price low to high"""
        inventory_page = InventoryPage(authenticated_page)
        
        inventory_page.sort_products(TestData.SORT_OPTIONS["price_low"])
        product_prices = inventory_page.get_product_prices()
        
        # Extract numeric values from price strings
        price_values = [float(price.replace('$', '')) for price in product_prices]
        
        # Verify prices are sorted low to high
        assert price_values == sorted(price_values)
    
    @pytest.mark.regression
    def test_sort_products_by_price_high_to_low(self, authenticated_page):
        """Test sorting products by price high to low"""
        inventory_page = InventoryPage(authenticated_page)
        
        inventory_page.sort_products(TestData.SORT_OPTIONS["price_high"])
        product_prices = inventory_page.get_product_prices()
        
        # Extract numeric values from price strings
        price_values = [float(price.replace('$', '')) for price in product_prices]
        
        # Verify prices are sorted high to low
        assert price_values == sorted(price_values, reverse=True)
    
    @pytest.mark.cart
    def test_add_single_product_to_cart(self, authenticated_page):
        """Test adding a single product to cart"""
        inventory_page = InventoryPage(authenticated_page)
        
        # Add backpack to cart
        inventory_page.add_product_to_cart("sauce-labs-backpack")
        
        # Verify cart badge shows 1
        assert inventory_page.get_cart_badge_count() == "1"
    
    @pytest.mark.cart
    def test_add_multiple_products_to_cart(self, authenticated_page):
        """Test adding multiple products to cart"""
        inventory_page = InventoryPage(authenticated_page)
        
        # Add multiple products
        inventory_page.add_product_to_cart("sauce-labs-backpack")
        inventory_page.add_product_to_cart("sauce-labs-bike-light")
        
        # Verify cart badge shows 2
        assert inventory_page.get_cart_badge_count() == "2"
    
    @pytest.mark.cart
    def test_remove_product_from_cart(self, authenticated_page):
        """Test removing product from cart"""
        inventory_page = InventoryPage(authenticated_page)
        
        # Add product then remove it
        inventory_page.add_product_to_cart("sauce-labs-backpack")
        assert inventory_page.get_cart_badge_count() == "1"
        
        inventory_page.remove_product_from_cart("sauce-labs-backpack")
        assert inventory_page.get_cart_badge_count() == "0"