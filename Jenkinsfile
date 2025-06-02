pipeline {
    agent any

    environment {
        SONARQUBE = credentials('sonarqube-token') // Your Sonar token credential ID
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
                echo 'Running pytest inside Docker...'
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
                    echo 'Running SonarQube scanner (ensure sonar-project.properties exists)'
                    // Uncomment when sonar-scanner is configured:
                    // sh 'sonar-scanner'
                }
            }
        }

        stage('Security') {
            steps {
                echo 'Running Bandit security scan...'
                sh '''
                    pip install bandit
                    bandit -r app
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Building and running Docker container...'
                sh '''
                    docker stop book_review_container || true
                    docker rm book_review_container || true
                    docker build -t book-review-app .
                    docker run -d -p 5000:5000 --name book_review_container book-review-app
                '''
            }
        }


        stage('Release') {
            steps {
                echo 'Tagging Docker image for release...'
                sh 'docker tag book-review-app book-review-app:v1.0'
            }
        }

        stage('Monitoring') {
            steps {
                echo 'Checking health endpoint...'
                sh 'curl -f http://localhost:5000/ || echo "Health check failed"'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up Docker container (if running)...'
            sh 'docker stop book-review-app || true'
            sh 'docker rm book-review-app || true'
        }
    }
}
