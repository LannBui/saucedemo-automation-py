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
    // 1) Produce a summary file using PowerShell (sandbox-safe)
    bat '''
      powershell -NoProfile -ExecutionPolicy Bypass -Command ^
        "$p = Join-Path $env:WORKSPACE 'reports\\junit.xml';" ^
        "if (Test-Path $p) {" ^
        "  [xml]$x = Get-Content -Raw $p;" ^
        "  $tests=0; $fail=0; $skip=0;" ^
        "  if ($x.testsuite) { $tests=[int]$x.testsuite.tests; $fail=[int]$x.testsuite.failures; $skip=[int]$x.testsuite.skipped }" ^
        "  elseif ($x.testsuites) { foreach ($s in $x.testsuites.testsuite) { $tests += [int]$s.tests; $fail += [int]$s.failures; $skip += [int]$s.skipped } }" ^
        "  \\"TOTAL=$tests`nFAILED=$fail`nSKIPPED=$skip\\" | Set-Content -NoNewline (Join-Path $env:WORKSPACE 'reports\\summary.txt');" ^
        "} else { \\"TOTAL=0`nFAILED=0`nSKIPPED=0\\" | Set-Content -NoNewline (Join-Path $env:WORKSPACE 'reports\\summary.txt'); }"
    '''

    script {
      // 2) Read the summary and build payload
      def txt = readFile("${env.WORKSPACE}\\reports\\summary.txt")

      def mTotal   = (txt =~ /TOTAL=(\d+)/)
      def mFailed  = (txt =~ /FAILED=(\d+)/)
      def mSkipped = (txt =~ /SKIPPED=(\d+)/)

      int total   = mTotal  ? mTotal[0][1].toInteger()  : 0
      int failed  = mFailed ? mFailed[0][1].toInteger() : 0
      int skipped = mSkipped? mSkipped[0][1].toInteger(): 0
      int passed  = total - failed - skipped
      int durSec  = (currentBuild.duration / 1000) as Integer

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

      // 3) POST to n8n; don’t fail build on notify issues
      try {
        def resp = httpRequest(
          httpMode: 'POST',
          url: N8N_WEBHOOK_URL,                   // http://localhost:5678/webhook/ci-summary
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
  }
  } // end post
} // end pipeline
