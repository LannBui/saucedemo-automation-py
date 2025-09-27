pipeline {
  agent any

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

    stage('Build Docker Image') {
      steps {
        sh 'docker build -t saucedemo-automation .'
      }
    }

    stage('Run Tests') {
      steps {
        sh '''
          mkdir -p reports allure-results
          docker run --rm \\
                 -v $(pwd)/reports:/app/reports \\
                 -v $(pwd)/allure-results:/app/allure-results \\
                 --entrypoint python \\
                 saucedemo-automation \\
                 -m pytest -m smoke --headless --incognito \\
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
