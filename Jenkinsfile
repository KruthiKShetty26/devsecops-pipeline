pipeline {
    agent any

    environment {
        IMAGE_NAME = 'devsecops-app'
        IMAGE_TAG = 'latest'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                bat 'pip install pytest && pytest tests/ -v'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube analysis...'
                withSonarQubeEnv('SonarQube') {
                    bat 'sonar-scanner -Dsonar.projectKey=devsecops-app -Dsonar.sources=. -Dsonar.host.url=http://sonarqube:9000'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                bat 'docker build -t %IMAGE_NAME%:%IMAGE_TAG% .'
            }
        }

        stage('Trivy Security Scan') {
            steps {
                echo 'Running Trivy security scan...'
                bat 'docker run --rm aquasec/trivy image --exit-code 1 --severity HIGH,CRITICAL %IMAGE_NAME%:%IMAGE_TAG%'
            }
        }

        stage('Run Container') {
            steps {
                echo 'Running container...'
                bat 'docker run -d -p 5000:5000 --name devsecops-app %IMAGE_NAME%:%IMAGE_TAG%'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished!'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}