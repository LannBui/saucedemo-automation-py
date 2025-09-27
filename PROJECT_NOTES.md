# 🚀 SauceDemo Automation - Project Notes & Commands

## 📋 Quick Reference Commands

### 🐳 Docker Commands

#### Build Docker Image
```bash
# Build the Docker image
docker build -t saucedemo-automation .

# Build with specific tag
docker build -t saucedemo-automation:latest .
docker build -t saucedemo-automation:v1.0 .
```

#### Run Docker Container
```bash
# Run all tests in Docker (headless + incognito)
docker run --rm --entrypoint python saucedemo-automation -m pytest tests/ --headless --incognito -v

# Run specific test suite in Docker
docker run --rm --entrypoint python saucedemo-automation -m pytest -m smoke --headless --incognito -v

# Run with different environment
docker run --rm -e ENVIRONMENT=staging --entrypoint python saucedemo-automation -m pytest tests/ --headless --incognito -v
docker run --rm -e ENVIRONMENT=prod --entrypoint python saucedemo-automation -m pytest tests/ --headless --incognito -v

# Run with Allure reporting
docker run --rm --entrypoint python saucedemo-automation -m pytest tests/ --headless --incognito --alluredir=allure-results
```

#### Docker Management
```bash
# List Docker images
docker images

# Remove Docker image
docker rmi saucedemo-automation

# Clean up unused Docker resources
docker system prune

# View Docker logs (if container is running)
docker logs <container_id>
```

### 📊 Allure Report Generation

#### Generate Allure Report
```bash
# Step 1: Run tests with Allure data collection
source venv/bin/activate && python -m pytest tests/ --headless --incognito --alluredir=allure-results

# Step 2: Generate HTML report
allure generate allure-results --clean -o allure-report

# Step 3: Open report in browser
allure open allure-report
```

#### Docker + Allure Report
```bash
# Step 1: Run tests in Docker with Allure
docker run --rm --entrypoint python saucedemo-automation -m pytest tests/ --headless --incognito --alluredir=allure-results

# Step 2: Generate report (run locally)
allure generate allure-results --clean -o allure-report

# Step 3: Open report
allure open allure-report
```

#### Allure Report Locations
- **Allure Results**: `allure-results/` directory (raw test data)
- **Allure Report**: `allure-report/` directory (HTML report)
- **Report URL**: `http://127.0.0.1:57778` (when opened with `allure open`)

### 🧪 Test Suite Management

#### Available Test Suites
```bash
# List all available test suites
python run_test_suite.py --list

# Available suites:
# - smoke: Critical functionality (9 tests)
# - login: Authentication tests (1 test)  
# - cart: Shopping cart tests
# - checkout: Checkout flow tests
# - navigation: Menu navigation tests
# - sort: Product sorting tests
# - critical: End-to-end critical path tests
# - regression: Comprehensive testing
# - full: Complete test suite (37 tests)
```

#### Run Test Suites
```bash
# Run specific test suite
python run_test_suite.py smoke --headless --incognito --verbose
python run_test_suite.py login --headless --incognito
python run_test_suite.py regression --headless --incognito --allure

# Run with different environments
python run_test_suite.py smoke --headless --incognito --env staging
python run_test_suite.py regression --headless --incognito --env prod
```

#### Direct pytest Commands
```bash
# Run with markers
python -m pytest -m smoke --headless --incognito -v
python -m pytest -m login --headless --incognito -v
python -m pytest -m regression --headless --incognito -v

# Run specific test files
python -m pytest tests/login/ --headless --incognito -v
python -m pytest tests/cart/ --headless --incognito -v
```

### 🌍 Environment Management

#### Environment Configuration
- **Dev**: `config/dev.properties` (default)
- **Staging**: `config/staging.properties`
- **Production**: `config/prod.properties`

#### Switch Environments
```bash
# Local execution
ENVIRONMENT=staging python -m pytest tests/ --headless --incognito -v
ENVIRONMENT=prod python -m pytest tests/ --headless --incognito -v

# Docker execution
docker run --rm -e ENVIRONMENT=staging --entrypoint python saucedemo-automation -m pytest tests/ --headless --incognito -v
docker run --rm -e ENVIRONMENT=prod --entrypoint python saucedemo-automation -m pytest tests/ --headless --incognito -v
```

### 🔧 Project Setup & Maintenance

#### Virtual Environment
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Update dependencies
pip install --upgrade -r requirements.txt
```

#### Configuration Files
- **Main Config**: `config/simple_config.py`
- **Environment Props**: `config/dev.properties`, `config/staging.properties`, `config/prod.properties`
- **Test Config**: `pytest.ini`
- **Docker Config**: `Dockerfile`

#### Key Directories
```
├── config/                 # Configuration files
├── tests/                  # Test files
│   ├── login/             # Login tests
│   ├── cart/              # Cart tests
│   ├── checkout/          # Checkout tests
│   ├── navigation/        # Navigation tests
│   └── sort/              # Sorting tests
├── pages/                  # Page Object Model
├── utils/                  # Utility functions
├── allure-results/         # Allure test results
├── allure-report/          # Allure HTML report
└── venv/                   # Virtual environment
```

### 🚀 Quick Start Commands

#### First Time Setup
```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Build Docker image
docker build -t saucedemo-automation .

# 3. Run smoke tests
python run_test_suite.py smoke --headless --incognito --verbose

# 4. Generate Allure report
python -m pytest tests/ --headless --incognito --alluredir=allure-results
allure generate allure-results --clean -o allure-report
allure open allure-report
```

#### Daily Development
```bash
# Run smoke tests (fast)
python run_test_suite.py smoke --headless --incognito

# Run specific test file
python -m pytest tests/login/valid_login_test.py --headless --incognito -v

# Run with Allure
python run_test_suite.py smoke --headless --incognito --allure
allure open allure-report
```

#### CI/CD Pipeline
```bash
# Build and test
docker build -t saucedemo-automation .
docker run --rm --entrypoint python saucedemo-automation -m pytest -m smoke --headless --incognito -v

# Full regression
docker run --rm --entrypoint python saucedemo-automation -m pytest tests/ --headless --incognito --alluredir=allure-results
```

### 📝 Important Notes

#### Docker Notes
- **Image Name**: `saucedemo-automation`
- **Default Environment**: `dev` (can be overridden with `-e ENVIRONMENT=staging`)
- **Entry Point**: `python` (overrides default `pytest`)
- **Headless Mode**: Required for Docker (no GUI available)

#### Allure Notes
- **Results Directory**: `allure-results/` (contains raw test data)
- **Report Directory**: `allure-report/` (contains HTML report)
- **Server URL**: `http://127.0.0.1:57778` (when opened)
- **Clean Generation**: Use `--clean` flag to overwrite existing reports

#### Test Suite Notes
- **Smoke Tests**: 9 tests, ~40 seconds (fast execution)
- **Login Tests**: 1 test, ~2 seconds (authentication only)
- **Full Suite**: 37 tests, ~2-3 minutes (complete testing)
- **Markers**: Use `@pytest.mark.smoke`, `@pytest.mark.login`, etc.

#### Configuration Notes
- **Environment Files**: Simple `.properties` format (key=value)
- **Default Environment**: `dev` (if not specified)
- **Browser**: Chrome (configurable per environment)
- **Credentials**: `standard_user` / `secret_sauce` (same for all environments)

### 🐛 Troubleshooting

#### Common Issues
```bash
# Docker daemon not running
open -a Docker

# Allure not installed
npm install -g allure-commandline

# Virtual environment not activated
source venv/bin/activate

# Permission issues
chmod +x run_test_suite.py
```

#### Useful Debug Commands
```bash
# Check Docker status
docker ps
docker images

# Check Allure installation
allure --version

# Check Python environment
python --version
pip list

# Check test collection
python -m pytest --collect-only
```

### 📚 Reference Links
- **Allure Documentation**: https://docs.qameta.io/allure/
- **pytest Documentation**: https://docs.pytest.org/
- **Docker Documentation**: https://docs.docker.com/
- **Selenium Documentation**: https://selenium-python.readthedocs.io/

---
**Last Updated**: $(date)
**Project**: SauceDemo Automation with Python + pytest + Docker + Allure
