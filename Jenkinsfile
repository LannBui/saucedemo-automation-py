pipeline {
  agent any

  environment {
    N8N_WEBHOOK_URL = 'http://localhost:5678/webhook/ci-summary'  // production URL
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
        // === CPS-safe JUnit summary ===
        def junitPath = "${env.WORKSPACE}\\reports\\junit.xml"
        int total = 0, failed = 0, skipped = 0

        try {
          if (fileExists(junitPath)) {
            def xmlText = readFile(junitPath)
            def xml = new XmlSlurper().parseText(xmlText)

            if (xml.name() == 'testsuite') {
              // Single suite
              total   = (xml.@tests?.text())    ? xml.@tests.toInteger()    : xml.testcase.size()
              failed  = (xml.@failures?.text()) ? xml.@failures.toInteger() : 0
              skipped = (xml.@skipped?.text())  ? xml.@skipped.toInteger()  : 0
            } else {
              // <testsuites> wrapper → iterate without spread operator
              total = 0; failed = 0; skipped = 0
              for (ts in xml.testsuite) {
                def t = ts.@tests?.text()
                def f = ts.@failures?.text()
                def s = ts.@skipped?.text()
                total   += t ? t.toInteger() : ts.testcase.size()
                failed  += f ? f.toInteger() : 0
                skipped += s ? s.toInteger() : 0
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

        // === Notify n8n (non-fatal if it fails) ===
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
      }

      echo 'Cleaning up...'
    }

    success  { echo 'Build succeeded with all tests passing.' }
    unstable { echo 'Build marked UNSTABLE due to test failures.' }
    failure  { echo 'Build failed due to critical errors.' }
  } // end post
} // end pipeline
