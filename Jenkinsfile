pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('test_run_cred')   // your Jenkins credential ID
        CLIENT_IMAGE = "dingus27/client"
        SERVER_IMAGE = "dingus27/server"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    docker.build("${CLIENT_IMAGE}:${env.BUILD_NUMBER}", "./client")
                    docker.build("${SERVER_IMAGE}:${env.BUILD_NUMBER}", "./server")
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        // Push client
                        docker.image("${CLIENT_IMAGE}:${env.BUILD_NUMBER}").push()
                        docker.image("${CLIENT_IMAGE}:${env.BUILD_NUMBER}").push("latest")

                        // Push server
                        docker.image("${SERVER_IMAGE}:${env.BUILD_NUMBER}").push()
                        docker.image("${SERVER_IMAGE}:${env.BUILD_NUMBER}").push("latest")
                    }
                }
            }
        }
    }
}
