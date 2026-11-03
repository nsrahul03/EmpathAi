pipeline {
    agent any

    environment {
        DOCKER = '/Users/shivarahulneelam/.docker/bin/docker'
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
                sh '/opt/homebrew/bin/python3.11 -m pip install pytest'
            }
        }

        stage('Run Tests') {
            steps {
                sh '/opt/homebrew/bin/python3.11 -m pytest -v'
            }
        }

        stage('Build Verification') {
            steps {
                sh '/opt/homebrew/bin/python3.11 -m py_compile web/app.py'
                echo 'Application build verification successful'
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
                    sleep 10
                    $DOCKER ps
                    curl --fail http://localhost:5002/
                '''
                echo 'Deployment successful!'
            }
        }
    }
}
