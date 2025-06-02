pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('SONAR_TOKEN')
        DOCKERHUB_CREDS = credentials('dockerhub-creds')
        DD_API_KEY = credentials('datadog-api-key')
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t book-review-app .'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests inside Docker container...'
                sh '''
                    docker run --rm \
                      -e PYTHONPATH=/app \
                      -v "$PWD":/app \
                      book-review-app \
                      bash -c "pytest --maxfail=1 --disable-warnings"
                '''
            }
        }

        stage('Code Quality') {
            steps {
                withSonarQubeEnv('SonarCloud') {
                    echo 'Running SonarQube scanner...'
                    sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=Su-Man_book-review-app \
                          -Dsonar.sources=app \
                          -Dsonar.host.url=https://sonarcloud.io \
                          -Dsonar.login=$SONAR_TOKEN
                    '''
                }
            }
        }

        stage('Security') {
            steps {
                echo 'Running Bandit inside Docker...'
                sh '''
                    docker run --rm \
                      -v "$PWD":/app \
                      book-review-app \
                      bash -c "pip install bandit && bandit -r app"
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Tagging Docker image with v1.0...'
                sh 'docker tag book-review-app sumangautam/book-review-app:1.0'

                echo 'Logging in to DockerHub...'
                sh 'echo $DOCKERHUB_CREDS_PSW | docker login -u $DOCKERHUB_CREDS_USR --password-stdin'

                echo 'Pushing image to DockerHub...'
                sh 'docker push sumangautam/book-review-app:1.0'

                echo 'Stopping any old container...'
                sh 'docker rm -f book-review-test || true'

                echo 'Running container on custom port 5050...'
                sh 'docker run -d --name book-review-test -p 5050:5000 sumangautam/book-review-app:1.0'
            }
        }

        stage('Release') {
            steps {
                echo 'Releasing version v1.0 to production...'
                sh 'docker tag book-review-app sumangautam/book-review-app:latest'
                sh 'docker push sumangautam/book-review-app:latest'
            }
        }

        stage('Monitoring') {
            steps {
                echo 'Sending health check to Datadog...'
                sh '''
                    curl --fail http://localhost:5050/health || echo "Service not responding on port 5050"
                    
                    curl -X POST "https://api.datadoghq.com/api/v1/events" \
                    -H "Content-Type: application/json" \
                    -H "DD-API-KEY: $DD_API_KEY" \
                    -d '{
                          "title": "Book Review App Deployment",
                          "text": "Health check passed on port 5050. Version 1.0 running in production.",
                          "alert_type": "info"
                        }'
                '''
            }
        }
    }
}
