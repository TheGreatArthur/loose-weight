pipeline {
  agent any

  options {
    timestamps()
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python') {
      steps {
        sh '''
          python3 --version
          python3 -m venv .venv
          . .venv/bin/activate
          python -m pip install --upgrade pip

          # Installe les dépendances si un requirements.txt existe
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt
          elif [ -f app/requirements.txt ]; then
            pip install -r app/requirements.txt
          else
            # au minimum pour lancer les tests
            pip install pytest
          fi

          # Installer les dépendances de développement (pytest)
          if [ -f requirements-dev.txt ]; then
            pip install -r requirements-dev.txt
          else
            pip install pytest
          fi
        '''
      }
    }

    stage('Run tests') {
      steps {
        sh '''
          . .venv/bin/activate
          # afficher la sortie standard du test pipeline (print) pour voir les RAW_INPUT et FLASH_MESSAGE
          pytest -s -q --junitxml=pytest-report.xml
        '''
      }
    }
  }

  post {
    always {
      junit allowEmptyResults: true, testResults: 'pytest-report.xml'
      archiveArtifacts artifacts: 'pytest-report.xml,pipeline-output.txt', fingerprint: true
    }
  }
}
