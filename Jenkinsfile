pipeline {
  agent any

  // 🔗 Put your n8n production webhook URL here
  environment {
    N8N_WEBHOOK_URL = 'http://localhost:5678/webhook/ci-summary'
  }

  options {
    timestamps()
    //ansiColor('xterm')
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
        // (Optional) switch to a venv later; OK to keep your current global python for now
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
        // ✅ Create 'reports' + produce both JUnit XML (for Jenkins) and HTML (for humans)
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
        // ✅ Publish results into Jenkins UI + keep HTML as artifact
        junit allowEmptyResults: true, testResults: 'reports/junit.xml'
        archiveArtifacts artifacts: 'reports/report.html', allowEmptyArchive: true
      }
    }
  }

  post {
    always {
      // ✅ Summarize from Jenkins' recorded JUnit data and POST to n8n
      script {
        def tra     = currentBuild.rawBuild.getAction(hudson.tasks.junit.TestResultAction)
        def total   = tra ? tra.totalCount : 0
        def failed  = tra ? tra.failCount  : 0
        def skipped = tra ? tra.skipCount  : 0
        def passed  = total - failed - skipped
        def payload = [
          job_name    : env.JOB_NAME,
          build_number: env.BUILD_NUMBER as Integer,
          build_url   : env.BUILD_URL,
          branch      : env.BRANCH_NAME ?: 'main',
          total       : total,
          passed      : passed,
          failed      : failed,
          skipped     : skipped,
          duration_sec: (currentBuild.duration/1000) as Integer,
          status      : currentBuild.currentResult
        ]
        def json = groovy.json.JsonOutput.toJson(payload)

        // Requires the "HTTP Request" plugin
        httpRequest httpMode: 'POST',
                    url: N8N_WEBHOOK_URL,
                    contentType: 'APPLICATION_JSON',
                    requestBody: json,
                    validResponseCodes: '200:299'
      }
      echo 'Cleaning up...'
    }
    success  { echo 'Build succeeded with all tests passing.' }
    unstable { echo 'Build marked UNSTABLE due to test failures.' }
    failure  { echo 'Build failed due to critical errors.' }
  }
}
