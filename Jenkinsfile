pipeline {
  agent {
    docker {
      image 'python:3.12-slim'
      args '-v /var/run/docker.sock:/var/run/docker.sock'
    }
  }

  environment {
    ENVIRONMENT = 'dev'
  }

  stages {
    stage('Checkout') {
      steps {
        git url: 'https://github.com/LannBui/saucedemo-automation-py.git',
            branch: 'main',
            credentialsId: 'github-token'
      }
    }

    stage('Install Dependencies') {
      steps {
        sh '''
          apt-get update && apt-get install -y --no-install-recommends \\
            chromium chromium-driver \\
            ca-certificates curl unzip \\
            fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 \\
            libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libglib2.0-0 libgtk-3-0 \\
            libnspr4 libnss3 libpango-1.0-0 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 \\
            libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 \\
            libxss1 libxtst6 xdg-utils build-essential gcc g++ libffi-dev libssl-dev \\
            && rm -rf /var/lib/apt/lists/*
          pip install --upgrade pip setuptools wheel
          pip install -r requirements.txt
        '''
      }
    }

    stage('Run Tests') {
      steps {
        sh '''
          mkdir -p reports allure-results
          export CHROME_BIN=/usr/bin/chromium
          export CHROMEDRIVER_PATH=/usr/bin/chromedriver
          python -m pytest -m smoke --headless --incognito \\
                 --junitxml=reports/junit.xml \\
                 --html=reports/report.html --self-contained-html \\
                 --alluredir=allure-results \\
                 -q
        '''
      }
    }

    stage('Archive Reports') {
      steps {
        junit allowEmptyResults: true, testResults: 'reports/junit.xml'
        archiveArtifacts artifacts: 'reports/report.html', allowEmptyArchive: true
      }
    }
  }

  post {
    always {
      sh '''
        if [ -d "allure-results" ]; then
          npm install -g allure-commandline
          allure generate allure-results --clean -o allure-report
          echo "Allure report generated"
        fi
      '''
      
      script {
        if (fileExists('allure-report')) {
          archiveArtifacts artifacts: 'allure-report/**', allowEmptyArchive: true
        }
      }
    }
  }
}
