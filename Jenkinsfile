pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'akiru091/resume-builder:latest'
        K8S_DEPLOYMENT = 'k8s/deployment.yaml'
        K8S_SERVICE = 'k8s/service.yaml'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/akiru-91/resume-builder.git'
            }
        }

        stage('Start Docker Desktop') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'open /Applications/Docker.app'  // For Mac
                    } else {
                        bat 'start "" "C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe"'  // For Windows
                    }
                }
                sleep(time: 20, unit: 'SECONDS')  // Wait for Docker to start
                sh 'docker --version'  // Verify Docker is running
            }
        }

        stage('Start Minikube') {
            steps {
                script {
                    sh 'minikube start --driver=docker'
                }
                sh 'minikube status'  // Verify Minikube is running
            }
        }

        stage('Install Dependencies & Run Tests') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pytest --junitxml=report.xml'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
                sh 'docker images'  // Verify image is built
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'docker-hub-credentials', url: 'https://index.docker.io/v1/']) {
                    sh 'docker push $DOCKER_IMAGE'
                }
                sh 'docker logout'  // Logout for security
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f $K8S_DEPLOYMENT'
                sh 'kubectl apply -f $K8S_SERVICE'
                sh 'kubectl get pods'  // Verify pods are running
                sh 'kubectl get services'  // Verify services are running
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    def pods = sh(script: 'kubectl get pods --selector=app=resume-app --no-headers | wc -l', returnStdout: true).trim()
                    echo "Running Pods: ${pods}"
                    if (pods == "0") {
                        error("No pods are running. Deployment failed.")
                    }

                    def service = sh(script: 'kubectl get svc resume-service --no-headers | wc -l', returnStdout: true).trim()
                    if (service == "0") {
                        error("Service is not running. Deployment failed.")
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'report.xml', fingerprint: true
        }
    }
}
