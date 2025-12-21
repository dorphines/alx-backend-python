pipeline {
    agent any

    environment {
        GITHUB_CREDS_ID = 'github-credentials'
        DOCKER_HUB_CREDS_ID = 'dockerhub-credentials'
        DOCKER_IMAGE = 'dorfin/messaging_app' 
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    credentialsId: "${GITHUB_CREDS_ID}", 
                    url: 'https://github.com/dorphines/alx-backend-python.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r messaging_app/requirements.txt
                pip install pytest pytest-django
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                mkdir -p reports
                export DJANGO_SETTINGS_MODULE=messaging_app.settings
                python3 -m pytest messaging_app/ \
                    -o "python_files=test_*.py *_test.py tests.py" \
                    --junitxml=reports/test-results.xml
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build \
                  --pull \
                  -t ${DOCKER_IMAGE}:${BUILD_ID} \
                  -t ${DOCKER_IMAGE}:latest \
                  messaging_app
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKER_HUB_CREDS_ID}",
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    docker logout || true
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                    for i in 1 2 3; do
                        docker push ${DOCKER_IMAGE}:${BUILD_ID} && break
                        echo "Retrying push... attempt $i"
                        sleep 10
                    done

                    docker push ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }
    }

    post {
        always {
            junit 'reports/test-results.xml'
        }
        cleanup {
            // Clean up the images so they don't clog your computer
            sh "docker rmi ${DOCKER_IMAGE}:${env.BUILD_ID} ${DOCKER_IMAGE}:latest || true"
        }
    }
}