# Test Suite Management Guide

## Overview

This guide explains how to manage test suites in Python (equivalent to TestNG groups in Java Selenium).

## 🎯 Allure Report Generation

### Generate Allure Report
```bash
# Run tests with Allure reporting
source venv/bin/activate && python -m pytest tests/ --headless --incognito --alluredir=allure-results

# Generate HTML report
allure generate allure-results --clean -o allure-report

# Open report in browser
allure open allure-report
```

### Docker with Allure
```bash
# Run tests in Docker with Allure
docker run --rm --entrypoint python saucedemo-automation -m pytest tests/ --headless --incognito --alluredir=allure-results

# Generate report (run locally after Docker execution)
allure generate allure-results --clean -o allure-report
allure open allure-report
```

## 🧪 Test Suite Management (Python equivalent of TestNG)

### Available Test Suites

| Suite | Description | Equivalent to TestNG |
|-------|-------------|---------------------|
| `smoke` | Critical functionality tests - fast execution | `groups="smoke"` |
| `regression` | Comprehensive testing - all functionality | `groups="regression"` |
| `login` | Authentication and login tests | `groups="login"` |
| `cart` | Shopping cart functionality tests | `groups="cart"` |
| `checkout` | Checkout flow and validation tests | `groups="checkout"` |
| `navigation` | Menu navigation and UI tests | `groups="navigation"` |
| `sort` | Product sorting functionality tests | `groups="sort"` |
| `critical` | End-to-end critical path tests | `groups="critical"` |
| `full` | Complete test suite - all tests | All groups |

### Running Test Suites

#### Method 1: Using Test Suite Runner (Recommended)
```bash
# List available suites
python run_test_suite.py --list

# Run specific suite
python run_test_suite.py smoke --headless --incognito --verbose
python run_test_suite.py login --headless --incognito
python run_test_suite.py regression --headless --incognito --allure

# With different environments
python run_test_suite.py smoke --headless --incognito --env staging
python run_test_suite.py regression --headless --incognito --env prod
```

#### Method 2: Direct pytest with markers
```bash
# Run smoke tests
python -m pytest -m smoke --headless --incognito -v

# Run login tests
python -m pytest -m login --headless --incognito -v

# Run regression tests
python -m pytest -m regression --headless --incognito -v

# Run multiple markers
python -m pytest -m "smoke or login" --headless --incognito -v
```

#### Method 3: Docker execution
```bash
# Smoke tests in Docker
docker run --rm --entrypoint python saucedemo-automation -m pytest -m smoke --headless --incognito -v

# Login tests in Docker
docker run --rm --entrypoint python saucedemo-automation -m pytest -m login --headless --incognito -v
```

### Test Markers in Code

```python
# Example test with multiple markers
@pytest.mark.smoke
@pytest.mark.login
@pytest.mark.critical
def test_valid_login(driver):
    # Test implementation
    pass

# Class-level markers
@pytest.mark.cart
@pytest.mark.regression
class TestCartCount:
    def test_add_product(self):
        # Test implementation
        pass
```

### Comparison: Java TestNG vs Python pytest

| Java TestNG | Python pytest | Description |
|-------------|----------------|-------------|
| `@Test(groups="smoke")` | `@pytest.mark.smoke` | Mark test as smoke test |
| `@Test(groups={"smoke", "login"})` | `@pytest.mark.smoke`<br>`@pytest.mark.login` | Multiple groups |
| `groups="smoke"` in XML | `-m smoke` in command | Run specific group |
| `groups={"smoke", "regression"}` | `-m "smoke or regression"` | Run multiple groups |
| XML suite files | `pytest.ini` + markers | Configuration |

### Test Suite Examples

#### Smoke Test Suite (Fast, Critical)
```bash
python run_test_suite.py smoke --headless --incognito
# Runs: 9 tests (login, cart basics, checkout flow)
```

#### Login Test Suite (Authentication)
```bash
python run_test_suite.py login --headless --incognito
# Runs: 1 test (valid login)
```

#### Regression Test Suite (Comprehensive)
```bash
python run_test_suite.py regression --headless --incognito
# Runs: All cart and checkout tests
```

#### Full Test Suite (Everything)
```bash
python run_test_suite.py full --headless --incognito
# Runs: All 37 tests
```

### CI/CD Integration

#### GitHub Actions Example
```yaml
name: Test Suites
on: [push, pull_request]

jobs:
  smoke-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Smoke Tests
        run: |
          python run_test_suite.py smoke --headless --incognito --allure
  
  regression-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Regression Tests
        run: |
          python run_test_suite.py regression --headless --incognito --allure
```

#### Jenkins Pipeline Example
```groovy
pipeline {
    agent any
    stages {
        stage('Smoke Tests') {
            steps {
                sh 'python run_test_suite.py smoke --headless --incognito'
            }
        }
        stage('Regression Tests') {
            steps {
                sh 'python run_test_suite.py regression --headless --incognito --allure'
            }
        }
    }
}
```

## 🚀 Quick Commands Reference

### Allure Reports
```bash
# Generate and view report
python -m pytest tests/ --alluredir=allure-results
allure generate allure-results --clean -o allure-report
allure open allure-report
```

### Test Suites
```bash
# List suites
python run_test_suite.py --list

# Run suites
python run_test_suite.py smoke --headless --incognito
python run_test_suite.py regression --headless --incognito --allure
python run_test_suite.py full --headless --incognito --env staging
```

### Docker
```bash
# Build and run
docker build -t saucedemo-automation .
docker run --rm --entrypoint python saucedemo-automation -m pytest -m smoke --headless --incognito -v
```

This system provides the same flexibility as TestNG groups but with Python's pytest framework! 🎉

