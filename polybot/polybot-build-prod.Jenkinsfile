pipeline {
    agent any


    environment {
        ECR_URL = "352708296901.dkr.ecr.us-east-2.amazonaws.com"

    }

    stages {
        stage('Build') {
            steps {
                sh '''
                pwd
                aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin $ECR_URL
                docker build -t edenb27-polybot-app:0.0.3 .
                docker push edenb27-jenkins:0.0.3
                '''
            }
            post {
                always {
                    sh 'docker image prune -a --force'
                }
            }
        }
    }
}
