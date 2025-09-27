"""
Test Suite Management - Python equivalent of TestNG groups
"""
from typing import List, Dict


class TestSuites:
    """Test suite configurations similar to TestNG groups"""
    
    # Smoke Test Suite - Critical functionality (like TestNG groups="smoke")
    SMOKE = [
        "tests/login/valid_login_test.py::test_valid_login",
        "tests/logout/logout_test.py::TestLogout::test_logout",
        "tests/cart/cart_count_test.py::TestCartCount::test_add_one_product_by_index",
        "tests/checkout/checkout_flow_test.py::TestCheckoutFlow::test_happy_path_checkout"
    ]
    
    # Regression Test Suite - Comprehensive testing (like TestNG groups="regression")
    REGRESSION = [
        "tests/login/",
        "tests/logout/",
        "tests/cart/",
        "tests/checkout/",
        "tests/navigation/",
        "tests/sort/"
    ]
    
    # Login Test Suite - Authentication related
    LOGIN = [
        "tests/login/"
    ]
    
    # Cart Test Suite - Shopping cart functionality
    CART = [
        "tests/cart/"
    ]
    
    # Checkout Test Suite - Checkout flow
    CHECKOUT = [
        "tests/checkout/"
    ]
    
    # Navigation Test Suite - Menu navigation
    NAVIGATION = [
        "tests/navigation/"
    ]
    
    # Sort Test Suite - Product sorting
    SORT = [
        "tests/sort/"
    ]
    
    # Critical Path Test Suite - End-to-end critical flows
    CRITICAL = [
        "tests/login/valid_login_test.py::test_valid_login",
        "tests/cart/cart_count_test.py::TestCartCount::test_add_one_product_by_index",
        "tests/checkout/checkout_flow_test.py::TestCheckoutFlow::test_happy_path_checkout",
        "tests/logout/logout_test.py::TestLogout::test_logout"
    ]
    
    # Full Test Suite - All tests
    FULL = [
        "tests/"
    ]
    
    @classmethod
    def get_suite_tests(cls, suite_name: str) -> List[str]:
        """Get test paths for a specific suite"""
        return getattr(cls, suite_name.upper(), cls.FULL)
    
    @classmethod
    def get_available_suites(cls) -> List[str]:
        """Get list of available test suites"""
        return [
            'smoke', 'regression', 'login', 'cart', 
            'checkout', 'navigation', 'sort', 'critical', 'full'
        ]
    
    @classmethod
    def get_suite_info(cls) -> Dict[str, str]:
        """Get information about each test suite"""
        return {
            'smoke': 'Critical functionality tests - fast execution',
            'regression': 'Comprehensive testing - all functionality',
            'login': 'Authentication and login tests',
            'cart': 'Shopping cart functionality tests',
            'checkout': 'Checkout flow and validation tests',
            'navigation': 'Menu navigation and UI tests',
            'sort': 'Product sorting functionality tests',
            'critical': 'End-to-end critical path tests',
            'full': 'Complete test suite - all tests'
        }


# Test Suite Runner
class TestSuiteRunner:
    """Run specific test suites"""
    
    def __init__(self, suite_name: str):
        self.suite_name = suite_name
        self.test_paths = TestSuites.get_suite_tests(suite_name)
    
    def get_pytest_command(self, additional_args: List[str] = None) -> List[str]:
        """Get pytest command for the test suite"""
        cmd = ['python', '-m', 'pytest']
        cmd.extend(self.test_paths)
        
        if additional_args:
            cmd.extend(additional_args)
        
        return cmd
    
    def run_suite(self, additional_args: List[str] = None):
        """Run the test suite"""
        import subprocess
        cmd = self.get_pytest_command(additional_args)
        return subprocess.run(cmd)


if __name__ == "__main__":
    # Example usage
    print("Available Test Suites:")
    for suite in TestSuites.get_available_suites():
        info = TestSuites.get_suite_info()[suite]
        print(f"  {suite}: {info}")
    
    print("\nExample: Run smoke tests")
    smoke_runner = TestSuiteRunner('smoke')
    print(f"Command: {' '.join(smoke_runner.get_pytest_command(['--headless', '--incognito']))}")

