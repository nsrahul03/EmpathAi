pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install CI Dependencies') {
            steps {
                sh '/opt/homebrew/bin/python3.11 -m pip install pytest'
            }
        }

        stage('Run Tests') {
            steps {
                sh '/opt/homebrew/bin/python3.11 -m pytest -v'
            }
        }

        stage('Build') {
            steps {
                sh '/opt/homebrew/bin/python3.11 -m py_compile web/app.py'
                echo 'Build completed successfully'
            }
        }
    }
}
