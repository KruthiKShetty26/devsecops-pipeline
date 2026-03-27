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
        catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
            sh 'echo "SonarQube analysis failed intentionally"'
            sh 'exit 1'
        }
    }
}

stage('Build Docker Image') {
    steps {
        catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
            sh 'echo "Docker build failed intentionally"'
            sh 'exit 1'
        }
    }
}

stage('Trivy Security Scan') {
    steps {
        catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
            sh 'echo "Trivy scan failed intentionally"'
            sh 'exit 1'
        }
    }
}

stage('Run Container') {
    steps {
        catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
            sh 'echo "Container run failed intentionally"'
            sh 'exit 1'
        }
    }
}