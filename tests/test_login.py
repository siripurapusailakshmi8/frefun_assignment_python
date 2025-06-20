import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.test_data import TestData

class TestLogin:
    
    @pytest.mark.login
    @pytest.mark.smoke
    def test_successful_login_standard_user(self, page):
        """Test successful login with standard user"""
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        
        login_page.login(TestData.STANDARD_USER, TestData.PASSWORD)
        
        assert inventory_page.is_inventory_displayed()
        assert "inventory.html" in page.url
    
    @pytest.mark.login
    @pytest.mark.negative
    def test_login_with_locked_out_user(self, page):
        """Test login with locked out user"""
        login_page = LoginPage(page)
        
        login_page.login(TestData.LOCKED_OUT_USER, TestData.PASSWORD)
        
        assert login_page.is_error_displayed()
        assert "locked out" in login_page.get_error_message().lower()
    
    @pytest.mark.login
    @pytest.mark.negative
    def test_login_with_invalid_credentials(self, page):
        """Test login with invalid credentials"""
        login_page = LoginPage(page)
        
        login_page.login(TestData.INVALID_USER, TestData.INVALID_PASSWORD)
        
        assert login_page.is_error_displayed()
        assert "username and password do not match" in login_page.get_error_message().lower()
    
    @pytest.mark.login
    @pytest.mark.negative
    def test_login_with_empty_username(self, page):
        """Test login with empty username"""
        login_page = LoginPage(page)
        
        login_page.login("", TestData.PASSWORD)
        
        assert login_page.is_error_displayed()
        assert "username is required" in login_page.get_error_message().lower()
    
    @pytest.mark.login
    @pytest.mark.negative
    def test_login_with_empty_password(self, page):
        """Test login with empty password"""
        login_page = LoginPage(page)
        
        login_page.login(TestData.STANDARD_USER, "")
        
        assert login_page.is_error_displayed()
        assert "password is required" in login_page.get_error_message().lower()
    
    @pytest.mark.login
    def test_logout_functionality(self, authenticated_page):
        """Test logout functionality"""
        inventory_page = InventoryPage(authenticated_page)
        login_page = LoginPage(authenticated_page)
        
        inventory_page.logout()
        
        # Should be back to login page
        assert authenticated_page.url == TestData.BASE_URL + "/"
        assert login_page.is_element_visible(login_page.LOGIN_BUTTON)