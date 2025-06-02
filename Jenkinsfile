pipeline {
    agent any
    environment {
        SONARQUBE = credentials('sonarqube-token') // optional
    }
    stages {
        stage('Build') {
            steps {
                echo 'Simulating build without Docker...'
                sh 'echo "Build stage: Flask app prepared."'
            }
        }
        stage('Test') {
            steps {
                echo 'Running pytest...'
                sh '''
                    pip install -r requirements.txt
                    export PYTHONPATH=$PYTHONPATH:$(pwd)
                    pytest --maxfail=1 --disable-warnings
            }
        }
        stage('Code Quality') {
            steps {
                withSonarQubeEnv('MySonarQubeServer') {
                    echo 'Skipping sonar-scanner (or enable if configured)'
                    // sh 'sonar-scanner'
                }
            }
        }
        stage('Security') {
            steps {
                echo 'Running Bandit security scan...'
                sh 'pip install bandit'
                sh 'bandit -r app'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Simulating deployment: app would start here.'
                sh 'echo "Running Flask app on http://localhost:5000 (simulated)"'
            }
        }
        stage('Release') {
            steps {
                echo 'Simulated production release'
                sh 'echo "Tagging v1.0 (simulated)"'
            }
        }
        stage('Monitoring') {
            steps {
                echo 'Monitoring stage: checking simulated health endpoint'
                sh 'echo "Health check passed (simulated)"'
            }
        }
    }
}
