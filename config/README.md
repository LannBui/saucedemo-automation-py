# Simplified Configuration System

This directory contains a simplified configuration system using property files for different environments.

## Files

- `simple_config.py` - Main configuration class
- `dev.properties` - Development environment settings
- `staging.properties` - Staging environment settings  
- `prod.properties` - Production environment settings

## Usage

### Basic Usage
```python
from config.simple_config import config

# Get configuration values
print(config.base_url)
print(config.username)
print(config.password)
print(config.browser)
print(config.headless)
```

### Environment Switching
```python
# Set environment via environment variable
import os
os.environ['ENVIRONMENT'] = 'staging'

# Or create config for specific environment
from config.simple_config import SimpleConfig
config = SimpleConfig('staging')
```

### Running Tests
```bash
# Run with default environment (dev)
python run_tests.py

# Run with specific environment
python run_tests.py --env staging

# Run with headless mode
python run_tests.py --env prod --headless
```

## Configuration Properties

Each environment file contains:

- **Environment Info**: `environment`, `base_url`
- **Credentials**: `username`, `password`
- **Browser Settings**: `browser`, `headless`, `incognito`, `window_width`, `window_height`
- **Timeouts**: `implicit_wait`, `page_load_timeout`, `script_timeout`
- **Test Settings**: `screenshot_on_failure`, `video_recording`, `parallel_workers`

## Benefits

1. **Simple**: Easy to understand and modify
2. **Clear**: All settings in one place per environment
3. **Maintainable**: No complex inheritance or classes
4. **Flexible**: Easy to add new properties or environments
