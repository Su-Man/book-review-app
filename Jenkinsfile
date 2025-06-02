pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('SONAR_TOKEN') // or 'sonarqube-token' if that's what you use
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
                echo 'Simulated Deployment'
                sh 'echo "Flask app would run on port 5000 inside container."'
            }
        }

        stage('Release') {
            steps {
                echo 'Simulated Release'
                sh 'echo "Tagging v1.0 for production (simulated)"'
            }
        }

        stage('Monitoring') {
            steps {
                echo 'Simulated Monitoring'
                sh 'echo "Health check passed (simulated)"'
            }
        }
    }
}
