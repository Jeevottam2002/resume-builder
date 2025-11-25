pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'jeevottam2002/resume-builder:latest'
        K8S_DEPLOYMENT = 'k8s/deployment.yaml'
        K8S_SERVICE = 'k8s/service.yaml'
        PYTHON = "C:\\Users\\Asus\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
        PIP = "C:\\Users\\Asus\\AppData\\Local\\Programs\\Python\\Python311\\Scripts\\pip.exe"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Jeevottam2002/resume-builder.git'
            }
        }

        stage('Start Docker Desktop') {
            steps {
                bat 'start "" "C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe"'
                sleep(time: 20, unit: 'SECONDS')
                bat 'docker --version'
            }
        }

        stage('Start Minikube') {
            steps {
                bat 'minikube start --driver=docker'
                bat 'minikube status'
            }
        }

        stage('Install Dependencies & Run Tests') {
            steps {
                bat '"%PIP%" install -r requirements.txt'
                bat '"%PYTHON%" -m pytest --junitxml=report.xml'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %DOCKER_IMAGE% .'
                bat 'docker images'
            }
        }

        stage('Push Docker Image') {
            steps {
                withDockerRegistry([credentialsId: 'docker-hub-creds', url: 'https://index.docker.io/v1/']) {
                    bat "docker push %DOCKER_IMAGE%"
                }
            }   // << FIXED — this was missing
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f %K8S_DEPLOYMENT%'
                bat 'kubectl apply -f %K8S_SERVICE%'
                bat 'kubectl get pods'
                bat 'kubectl get svc'
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    def pods = bat(script: 'kubectl get pods --no-headers | find /c /v ""', returnStdout: true).trim()
                    echo "Running Pods: ${pods}"
                    if (pods == "0") {
                        error("❌ No Kubernetes Pods Running!")
                    }

                    def services = bat(script: 'kubectl get svc resume-service --no-headers | find /c /v ""', returnStdout: true).trim()
                    if (services == "0") {
                        error("❌ Kubernetes Service Not Running!")
                    }
                }
            }
        }
    }  // << closes stages block

    post {   // << post must be INSIDE pipeline (fixed)
        always {
            archiveArtifacts artifacts: 'report.xml', fingerprint: true
        }
        success {
            echo "🚀 Build & Deployment Completed Successfully!"
        }
        failure {
            echo "❌ Build Failed! Check Logs!"
        }
    }
}
