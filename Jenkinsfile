pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }

    environment {
        APP_NAME = 'warehouse-api'
    }

    stages {
        stage('1. Run PyTest Tests') {
            steps {
                echo "=== Running Unit Tests ==="
                sh '''
                    python3 -m venv /tmp/venv
                    /tmp/venv/bin/pip install --upgrade pip
                    /tmp/venv/bin/pip install -r requirements.txt
                    /tmp/venv/bin/pytest -v test_main.py
                '''
            }
        }

        stage('2. Build Docker Image') {
            steps {
                echo "=== Building Docker Image ==="
                sh '''
                    COMMIT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "v1.0.0")
                    echo "Building with tag: ${COMMIT_SHA}"
                    docker build -t ${APP_NAME}:${COMMIT_SHA} .
                    docker tag ${APP_NAME}:${COMMIT_SHA} ${APP_NAME}:latest
                '''
            }
        }

        stage('3. Security Vulnerability Scan') {
            steps {
                echo "=== Running Trivy Security Scan ==="
                sh '''
                    if command -v trivy &> /dev/null; then
                        trivy image --severity HIGH,CRITICAL --exit-code 0 ${APP_NAME}:latest
                    else
                        echo "⚠️ Trivy binary not found, skipping security gate"
                    fi
                '''
            }
        }

        stage('4. Load into Cluster') {
            steps {
                echo "=== Loading Image into Kind Cluster ==="
                sh '''
                    COMMIT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "v1.0.0")
                    kind load docker-image ${APP_NAME}:${COMMIT_SHA} --name gitops-cluster || true
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline Build Succeeded! Ready for GitOps deployment."
        }
        failure {
            echo "❌ Pipeline Failed!"
        }
    }
}
