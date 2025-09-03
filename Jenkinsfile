pipeline {
  agent any

  environment {
    N8N_WEBHOOK_URL = 'http://localhost:5678/webhook/ci-summary'
  }

  options {
    timestamps()
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

    stage('Run Pytest') {
      steps {
        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
          bat '''
            if not exist reports mkdir reports
            pytest --headless --incognito ^
                   --junitxml=reports\\junit.xml ^
                   --html=reports\\report.html --self-contained-html ^
                   -q
          '''
        }
      }
    }

    stage('Archive Reports') {
      steps {
        junit allowEmptyResults: true, testResults: 'reports/junit.xml'
        archiveArtifacts artifacts: 'reports/report.html', allowEmptyArchive: true
      }
    }
  } // end stages

  post {
    always {
      script {
        // --- Read junit.xml (sandbox-friendly, no rawBuild) ---
        def junitPath = "${env.WORKSPACE}\\reports\\junit.xml"
        int total = 0, failed = 0, skipped = 0

        try {
          def file = new File(junitPath)
          if (file.exists()) {
            def xml = new XmlSlurper().parse(file)

            if (xml.name() == 'testsuite') {
              total   = (xml.@tests?.text())    ? xml.@tests.toInteger()    : xml.testcase.size()
              failed  = (xml.@failures?.text()) ? xml.@failures.toInteger() : 0
              skipped = (xml.@skipped?.text())  ? xml.@skipped.toInteger()  : 0
            } else {
              // <testsuites> wrapper
              if (xml.@tests?.text()) {
                total   = xml.@tests.toInteger()
                failed  = (xml.@failures?.text()) ? xml.@failures.toInteger() : 0
                skipped = (xml.@skipped?.text())  ? xml.@skipped.toInteger()  : 0
              } else {
                total   = (xml.testsuite*.@tests*.toInteger()).sum()    ?: 0
                failed  = (xml.testsuite*.@failures*.toInteger()).sum() ?: 0
                skipped = (xml.testsuite*.@skipped*.toInteger()).sum()  ?: 0
              }
            }
          } else {
            echo "junit.xml not found at: ${junitPath}"
          }
        } catch (e) {
          echo "Could not parse junit.xml: ${e.message}"
        }

        int passed = total - failed - skipped
        int durSec = (currentBuild.duration / 1000) as Integer
        def payload = [
          job_name    : env.JOB_NAME,
          build_number: (env.BUILD_NUMBER ?: "0") as Integer,
          build_url   : env.BUILD_URL,
          branch      : env.BRANCH_NAME ?: 'main',
          total       : total,
          passed      : passed,
          failed      : failed,
          skipped     : skipped,
          duration_sec: durSec,
          status      : currentBuild.currentResult
        ]
        def json = groovy.json.JsonOutput.toJson(payload)

        // --- POST to n8n; do not fail the build if notification fails ---
        try {
          def resp = httpRequest(
            httpMode: 'POST',
            url: N8N_WEBHOOK_URL,
            contentType: 'APPLICATION_JSON',
            requestBody: json,
            timeout: 30,
            validResponseCodes: '200:299'
          )
          echo "n8n webhook response: ${resp.status}"
        } catch (e) {
          echo "⚠️ n8n webhook failed: ${e.message}"
          currentBuild.result = currentBuild.result ?: 'UNSTABLE'
        }
      } // end script

      echo 'Cleaning up...'
    } // end always

    success  { echo 'Build succeeded with all tests passing.' }
    unstable { echo 'Build marked UNSTABLE due to test failures.' }
    failure  { echo 'Build failed due to critical errors.' }
  } // end post
} // end pipeline
