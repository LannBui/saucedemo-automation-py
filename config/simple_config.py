"""
Simple configuration management using property files
"""
import os
from typing import Dict, Any


class SimpleConfig:
    """Simple configuration class that reads from property files"""
    
    def __init__(self, environment: str = None):
        """
        Initialize configuration
        
        Args:
            environment: Environment name (dev, staging, prod)
        """
        self.environment = environment or os.getenv('ENVIRONMENT', 'dev')
        self._properties = self._load_properties()
    
    def _load_properties(self) -> Dict[str, str]:
        """Load properties from environment-specific file"""
        properties_file = f'config/{self.environment}.properties'
        properties = {}
        
        if os.path.exists(properties_file):
            with open(properties_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            properties[key.strip()] = value.strip()
        
        return properties
    
    def get(self, key: str, default: str = None) -> str:
        """Get property value"""
        return self._properties.get(key, default)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get property value as integer"""
        try:
            return int(self.get(key, str(default)))
        except ValueError:
            return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get property value as boolean"""
        value = self.get(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    def get_tuple(self, key: str, default: tuple = (1920, 1080)) -> tuple:
        """Get property value as tuple (for window size)"""
        try:
            width = self.get_int('window_width', default[0])
            height = self.get_int('window_height', default[1])
            return (width, height)
        except:
            return default
    
    # Convenience properties
    @property
    def base_url(self) -> str:
        """Get base URL"""
        return self.get('base_url', 'https://www.saucedemo.com')
    
    @property
    def username(self) -> str:
        """Get username"""
        return self.get('username', 'standard_user')
    
    @property
    def password(self) -> str:
        """Get password"""
        return self.get('password', 'secret_sauce')
    
    @property
    def browser(self) -> str:
        """Get browser name"""
        return self.get('browser', 'chrome')
    
    @property
    def headless(self) -> bool:
        """Get headless setting"""
        return self.get_bool('headless', False)
    
    @property
    def incognito(self) -> bool:
        """Get incognito setting"""
        return self.get_bool('incognito', False)
    
    @property
    def window_size(self) -> tuple:
        """Get window size"""
        return self.get_tuple('window_size', (1920, 1080))
    
    @property
    def implicit_wait(self) -> int:
        """Get implicit wait timeout"""
        return self.get_int('implicit_wait', 10)
    
    @property
    def page_load_timeout(self) -> int:
        """Get page load timeout"""
        return self.get_int('page_load_timeout', 30)
    
    @property
    def script_timeout(self) -> int:
        """Get script timeout"""
        return self.get_int('script_timeout', 30)
    
    @property
    def screenshot_on_failure(self) -> bool:
        """Get screenshot on failure setting"""
        return self.get_bool('screenshot_on_failure', True)
    
    @property
    def video_recording(self) -> bool:
        """Get video recording setting"""
        return self.get_bool('video_recording', False)
    
    @property
    def parallel_workers(self) -> int:
        """Get parallel workers count"""
        return self.get_int('parallel_workers', 1)


# Global configuration instance
config = SimpleConfig()

