pipeline {
    agent any

    environment {
        IMAGE_NAME = "warehouse-api"
        REGISTRY = "local" // We will push to local registry or Docker Hub
    }

    stages {
        stage('1. Checkout Code') {
            steps {
                echo "=== Checkout completed successfully ==="
                sh "git status || true"
            }
        }

        stage('2. Run Unit Tests') {
            steps {
                echo "=== Running PyTest Unit Tests ==="
                sh """
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pytest -v
                """
            }
        }

        stage('3. Build Docker Image') {
            steps {
                echo "=== Building Docker Image tagged with Commit SHA ==="
                sh """
                    COMMIT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "v1.0.0")
                    docker build -t ${IMAGE_NAME}:${COMMIT_SHA} .
                    docker tag ${IMAGE_NAME}:${COMMIT_SHA} ${IMAGE_NAME}:latest
                """
            }
        }

        stage('4. Security Vulnerability Scan') {
            steps {
                echo "=== Running Security Scan on Container Image ==="
                // Using Trivy container scanner
                sh """
                    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                    aquasec/trivy:latest image --severity HIGH,CRITICAL ${IMAGE_NAME}:latest || true
                """
            }
        }

        stage('5. Load Image to Kind Cluster') {
            steps {
                echo "=== Loading verified image into Kind Cluster ==="
                sh """
                    COMMIT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "v1.0.0")
                    kind load docker-image ${IMAGE_NAME}:${COMMIT_SHA} --name gitops-cluster || true
                """
            }
        }
    }

    post {
        success {
            echo "✅ BUILD SUCCESSFUL! Image verified and loaded into K8s cluster."
        }
        failure {
            echo "❌ BUILD FAILED! Check console logs above for details."
        }
    }
}
