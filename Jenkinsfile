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
                sh 'pip3 install -r requirements.txt || python3 -m pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                sh 'pip3 install pytest && python3 -m pytest tests/ -v'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube analysis...'
                withSonarQubeEnv('SonarQube') {
                    sh 'sonar-scanner -Dsonar.projectKey=devsecops-app -Dsonar.sources=. -Dsonar.host.url=http://sonarqube:9000 || echo "SonarQube scan skipped"'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
            }
        }
        stage('Trivy Security Scan') {
            steps {
                echo 'Running Trivy security scan...'
                sh 'docker run --rm aquasec/trivy image --exit-code 0 --severity HIGH,CRITICAL $IMAGE_NAME:$IMAGE_TAG'
            }
        }
        stage('Run Container') {
            steps {
                echo 'Running container...'
                sh 'docker stop devsecops-app || true'
                sh 'docker rm devsecops-app || true'
                sh 'docker run -d -p 5000:5000 --name devsecops-app $IMAGE_NAME:$IMAGE_TAG'
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