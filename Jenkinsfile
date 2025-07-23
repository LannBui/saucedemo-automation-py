pipeline {
    agent any

    environment {

    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/LannBui/saucedemo-automation-py.git',
                    branch: 'main',
                    credentialsId: 'mlan-github-creds'
            }
        }

        stage('Set up Python') {
            steps {
                // Print Python version for debugging
                bat 'python --version'
                bat 'pip --version'
            }
        }

        stage('Install dependencies') {
            steps {
                bat 'pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run Pytest') {
            steps {
                // Run your tests in headless and incognito mode
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    bat 'pytest --headless --incognito --html=reports/report.html'
                }
            }
        }

        stage('Archive Reports') {
            steps {
                // Archive the HTML report
                archiveArtifacts artifacts: 'reports/report.html', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
        }
        success {
            echo 'Build succeeded with all tests passing.'
        }
        unstable {
            echo 'Build marked UNSTABLE due to test failures (e.g., assertions).'
        }
        failure {
            echo 'Build failed due to critical errors (e.g., install or pytest failure).'
        }
    }
}