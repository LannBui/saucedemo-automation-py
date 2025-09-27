# 🚀 Jenkins Pipeline Setup Guide

## 📋 Updated Jenkinsfile Features

### ✅ **Removed n8n Integration**
- Removed n8n webhook configuration
- Simplified post-build actions
- Focus on test execution and reporting

### 🎯 **New Pipeline Parameters**
- **TEST_SUITE**: Choose test suite (smoke, regression, login, cart, checkout, full)
- **ENVIRONMENT**: Select environment (dev, staging, prod)
- **RUN_DOCKER_TESTS**: Optional Docker testing
- **GENERATE_ALLURE_REPORT**: Enable/disable Allure reporting

### 🔄 **Pipeline Stages**

#### 1. **Checkout**
- Git repository checkout
- Branch-based environment detection

#### 2. **Environment Setup**
- Automatic environment detection based on branch
- Parameter override support
- Environment logging

#### 3. **Python Setup**
- Python version verification
- Dependency installation

#### 4. **Run Tests**
- Uses simplified test suite runner
- Parameterized test execution
- JUnit and HTML report generation
- Optional Allure reporting

#### 5. **Docker Test (Optional)**
- Conditional Docker testing
- Environment variable passing
- Separate Docker reports

#### 6. **Archive Reports**
- JUnit results archiving
- HTML report archiving
- Docker report archiving (if available)

#### 7. **Post-Build Actions**
- Allure report generation
- Report archiving
- Status notifications

## 🚀 **Usage Examples**

### **Basic Smoke Test Run**
```groovy
// Parameters:
// TEST_SUITE: smoke
// ENVIRONMENT: dev
// RUN_DOCKER_TESTS: false
// GENERATE_ALLURE_REPORT: true
```

### **Full Regression with Docker**
```groovy
// Parameters:
// TEST_SUITE: regression
// ENVIRONMENT: staging
// RUN_DOCKER_TESTS: true
// GENERATE_ALLURE_REPORT: true
```

### **Production Testing**
```groovy
// Parameters:
// TEST_SUITE: full
// ENVIRONMENT: prod
// RUN_DOCKER_TESTS: false
// GENERATE_ALLURE_REPORT: true
```

## 📊 **Report Generation**

### **JUnit Reports**
- **Local**: `reports/junit.xml`
- **Docker**: `reports/junit-docker.xml`
- **Jenkins Integration**: Automatic test result parsing

### **HTML Reports**
- **Local**: `reports/report.html`
- **Docker**: `reports/report-docker.html`
- **Archived**: Available in Jenkins build artifacts

### **Allure Reports**
- **Results**: `allure-results/` (raw data)
- **Report**: `allure-report/` (HTML report)
- **Archived**: Available in Jenkins build artifacts

## 🔧 **Configuration**

### **Environment Detection**
```groovy
// Automatic detection:
// main branch → prod environment
// staging branch → staging environment
// other branches → dev environment

// Manual override:
// Use ENVIRONMENT parameter
```

### **Test Suite Selection**
```groovy
// Available suites:
// - smoke: Critical functionality (9 tests)
// - regression: Comprehensive testing
// - login: Authentication tests
// - cart: Shopping cart tests
// - checkout: Checkout flow tests
// - full: Complete test suite (37 tests)
```

### **Docker Integration**
```groovy
// Optional Docker testing:
// - Builds Docker image
// - Runs tests in container
// - Generates separate reports
// - Environment variable passing
```

## 📝 **Jenkins Job Configuration**

### **Required Plugins**
- **Pipeline**: For Jenkinsfile support
- **JUnit**: For test result parsing
- **HTML Publisher**: For HTML report display
- **Allure**: For Allure report integration (optional)

### **Job Setup**
1. **Create Pipeline Job**
2. **Configure Git Repository**
3. **Set Jenkinsfile Path**: `Jenkinsfile`
4. **Enable Parameterized Build**
5. **Configure Build Triggers**

### **Build Parameters**
```groovy
// Default values:
// TEST_SUITE: smoke
// ENVIRONMENT: dev
// RUN_DOCKER_TESTS: false
// GENERATE_ALLURE_REPORT: true
```

## 🎯 **Best Practices**

### **Branch Strategy**
- **main**: Production environment, full test suite
- **staging**: Staging environment, regression tests
- **feature/***: Development environment, smoke tests

### **Test Execution**
- **Smoke Tests**: Fast feedback, run on every commit
- **Regression Tests**: Comprehensive testing, run on merge
- **Full Suite**: Complete testing, run on release

### **Report Management**
- **JUnit**: For Jenkins test result parsing
- **HTML**: For detailed test reports
- **Allure**: For advanced reporting and analytics

## 🐛 **Troubleshooting**

### **Common Issues**
```bash
# Python not found
# Solution: Install Python plugin or configure PATH

# Docker not available
# Solution: Install Docker plugin or disable Docker tests

# Allure not installed
# Solution: Install Allure plugin or disable Allure reports
```

### **Debug Commands**
```groovy
// Add to pipeline for debugging:
echo "Environment: ${env.ENVIRONMENT}"
echo "Test Suite: ${params.TEST_SUITE}"
echo "Docker Tests: ${params.RUN_DOCKER_TESTS}"
echo "Allure Report: ${params.GENERATE_ALLURE_REPORT}"
```

## 📚 **Reference**

### **Pipeline Syntax**
- **Parameters**: `params.PARAMETER_NAME`
- **Environment**: `env.ENVIRONMENT`
- **Conditions**: `when { expression { condition } }`
- **Scripts**: `script { groovy code }`

### **File Paths**
- **Windows**: Use `\\` for path separators
- **Reports**: `reports\\filename.xml`
- **Allure**: `allure-results\\`, `allure-report\\`

---
**Last Updated**: $(date)
**Pipeline**: SauceDemo Automation with Jenkins + Docker + Allure
