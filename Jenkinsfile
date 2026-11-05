pipeline {

    agent any

    environment {
        DOCKER = '/Users/shivarahulneelam/.docker/bin/docker'
        PYTHON = '/opt/homebrew/bin/python3.11'

        IMAGE_NAME = 'empath-ai:1.0'
        CONTAINER_NAME = 'empath-ai-container'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    $PYTHON -m pip install pytest selenium
                '''
            }
        }

        stage('Unit Testing') {
            steps {
                sh '''
                    $PYTHON -m pytest -v test_app.py
                '''
            }
        }

        stage('Build Verification') {
            steps {
                sh '''
                    $PYTHON -m py_compile web/app.py
                '''

                echo 'Application build successful'
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    $DOCKER build -t $IMAGE_NAME .
                '''
            }
        }

        stage('Docker Deploy') {
            steps {
                sh '''
                    $DOCKER rm -f $CONTAINER_NAME || true

                    $DOCKER run -d \
                        --name $CONTAINER_NAME \
                        --restart unless-stopped \
                        -p 5002:5000 \
                        $IMAGE_NAME
                '''
            }
        }

        stage('Deployment Verification') {
            steps {
                sh '''
                    sleep 15

                    $DOCKER ps

                    curl --fail http://localhost:5002/
                '''

                echo 'Deployment successful'
            }
        }

        stage('Selenium UI Testing') {
    steps {
        sh '/opt/homebrew/bin/python3.11 -m pytest -v test_selenium.py'
    }
}

    }

    post {
        always {
            archiveArtifacts artifacts: 'selenium_empath_ai.png',
                             allowEmptyArchive: true
        }

        success {
            echo 'EMPATH AI CI/CD PIPELINE COMPLETED SUCCESSFULLY'
        }

        failure {
            echo 'PIPELINE FAILED - CHECK CONSOLE OUTPUT'
        }
    }
}