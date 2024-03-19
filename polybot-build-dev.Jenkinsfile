pipeline {
    agent any


    environment {
        ECR_URL = "352708296901.dkr.ecr.us-east-2.amazonaws.com"
        IMAGE_NAME = "edenb27-polybot-app"

    }

    stages {
        stage('Build') {
            steps {

                sh '''
                cd polybot
                aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin $ECR_URL
                docker build -t $IMAGE_NAME:0.0.7 .
                docker tag $IMAGE_NAME:0.0.7 $ECR_URL/$IMAGE_NAME:0.0.7
                docker push  $ECR_URL/$IMAGE_NAME:0.0.7
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
