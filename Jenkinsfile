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
                sh 'echo "Dependencies installed successfully"'
            }
        }
        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                sh 'echo "All tests passed successfully"'
            }
        }
        stage('SonarQube Analysis') {
    		steps {
        		echo "Running SonarQube analysis..."
        		sh 'exit 1'
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
                sh '''
                    docker run --rm aquasec/trivy image \
                    --exit-code 1 \
                    --severity HIGH,CRITICAL \
                    --no-progress \
                    $IMAGE_NAME:$IMAGE_TAG
                '''
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
            echo 'Pipeline failed! Notifying team...'
        }
    }
}
```

Save it, then run:
```
git add Jenkinsfile
git commit -m "Demo - SonarQube quality gate failure"
git push origin main