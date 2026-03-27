pipeline {
    agent any

    stages {

        stage('Checkout SCM') {
            steps {
                git 'https://github.com/your-repo.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'echo "Running tests..."'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                sh 'echo "SonarQube failed"'
                sh 'exit 1'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'echo "Docker build failed"'
                sh 'exit 1'
            }
        }

        stage('Trivy Security Scan') {
            steps {
                sh 'echo "Security scan failed"'
                sh 'exit 1'
            }
        }

        stage('Run Container') {
            steps {
                sh 'echo "Container failed to run"'
                sh 'exit 1'
            }
        }

    }
}