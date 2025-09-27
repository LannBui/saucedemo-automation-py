pipeline {
  agent any

  parameters {
    choice(
      name: 'TEST_SUITE',
      choices: ['smoke', 'regression', 'login', 'cart', 'checkout', 'full'],
      description: 'Select test suite to run'
    )
    choice(
      name: 'ENVIRONMENT',
      choices: ['dev', 'staging', 'prod'],
      description: 'Select environment to test against'
    )
    booleanParam(
      name: 'RUN_DOCKER_TESTS',
      defaultValue: false,
      description: 'Run tests in Docker container'
    )
    booleanParam(
      name: 'GENERATE_ALLURE_REPORT',
      defaultValue: true,
      description: 'Generate Allure report'
    )
  }

  environment {
    // Make webdriver-manager use cached drivers (recommended on corp/VPN networks)
    WDM_OFFLINE = 'true'
    WDM_LOCAL   = 'true'

    // If you need a pinned chromedriver, set this and point driver_factory.py to use it when present:
    // CHROMEDRIVER_PATH = "${WORKSPACE}\\bin\\chromedriver.exe"

    // If you need proxy for Python/requests and webdriver-manager, uncomment and set:
    // HTTP_PROXY  = 'http://proxy:port'
    // HTTPS_PROXY = 'http://proxy:port'
    // REQUESTS_CA_BUNDLE = 'C:\\path\\to\\corp-ca.pem'
  }

  options { timestamps() }

  stages {
    stage('Checkout') {
      steps {
        git url: 'https://github.com/LannBui/saucedemo-automation-py.git',
            branch: 'main',
            credentialsId: 'mlan-github-creds'
      }
    }

    stage('Environment Setup') {
      steps {
        script {
          // Use parameter or set based on branch
          if (params.ENVIRONMENT) {
            env.ENVIRONMENT = params.ENVIRONMENT
          } else if (env.BRANCH_NAME == 'main') {
            env.ENVIRONMENT = 'prod'
          } else if (env.BRANCH_NAME == 'staging') {
            env.ENVIRONMENT = 'staging'
          } else {
            env.ENVIRONMENT = 'dev'
          }
          echo "Running tests against ${env.ENVIRONMENT} environment"
          echo "Test suite: ${params.TEST_SUITE}"
        }
      }
    }

    stage('Set up Python') {
      steps {
        bat 'python --version'
        bat 'pip --version'
      }
    }

    stage('Install dependencies') {
      steps {
        bat 'python -m pip install --upgrade pip'
        bat 'pip install -r requirements.txt'
      }
    }

    stage('Run Tests') {
      steps {
        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
          script {
            def allureFlag = params.GENERATE_ALLURE_REPORT ? '--allure' : ''
            def testSuite = params.TEST_SUITE ?: 'smoke'
            
            bat """
              if not exist reports mkdir reports
              python run_test_suite.py ${testSuite} --headless --incognito ^
                     --junitxml=reports\\junit.xml ^
                     --html=reports\\report.html --self-contained-html ^
                     ${allureFlag} ^
                     -q
            """
          }
        }
      }
    }

    stage('Docker Test (Optional)') {
      when {
        expression { params.RUN_DOCKER_TESTS == true }
      }
      steps {
        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
          script {
            def testSuite = params.TEST_SUITE ?: 'smoke'
            def allureFlag = params.GENERATE_ALLURE_REPORT ? '--alluredir=allure-results-docker' : ''
            
            // Build Docker image
            bat 'docker build -t saucedemo-automation .'
            
            // Run tests in Docker
            bat """
              docker run --rm -e ENVIRONMENT=${env.ENVIRONMENT} --entrypoint python saucedemo-automation -m pytest -m ${testSuite} --headless --incognito ^
                     --junitxml=reports\\junit-docker.xml ^
                     --html=reports\\report-docker.html --self-contained-html ^
                     ${allureFlag} ^
                     -q
            """
          }
        }
      }
    }

    stage('Archive Reports') {
      steps {
        // Archive JUnit results
        junit allowEmptyResults: true, testResults: 'reports/junit.xml'
        
        // Archive HTML reports
        archiveArtifacts artifacts: 'reports/report.html', allowEmptyArchive: true
        
        // Archive Docker reports if they exist
        script {
          if (fileExists('reports/junit-docker.xml')) {
            junit allowEmptyResults: true, testResults: 'reports/junit-docker.xml'
          }
          if (fileExists('reports/report-docker.html')) {
            archiveArtifacts artifacts: 'reports/report-docker.html', allowEmptyArchive: true
          }
        }
      }
    }
  } // end stages

  post {
    always {
      // Generate Allure report if allure-results exist
      script {
        if (fileExists('allure-results')) {
          bat '''
            if exist allure-results (
              echo "Generating Allure report..."
              allure generate allure-results --clean -o allure-report
              echo "Allure report generated in allure-report directory"
            )
          '''
        }
      }

      // Archive Allure report if it exists
      script {
        if (fileExists('allure-report')) {
          archiveArtifacts artifacts: 'allure-report/**', allowEmptyArchive: true
          echo "Allure report archived"
        }
      }

      echo 'Pipeline completed. Check reports for detailed results.'
    }

    success  { 
      echo '✅ Build succeeded with all tests passing.' 
      echo '📊 Check the archived reports for detailed test results.'
    }
    unstable { 
      echo '⚠️ Build marked UNSTABLE due to test failures.' 
      echo '📊 Check the archived reports for detailed test results.'
    }
    failure  { 
      echo '❌ Build failed due to critical errors.' 
      echo '📊 Check the archived reports for detailed test results.'
    }
  } // end post
} // end pipeline
