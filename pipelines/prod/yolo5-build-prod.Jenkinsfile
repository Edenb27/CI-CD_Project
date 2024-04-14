pipeline {
    agent any


    environment {
        ECR_URL = "352708296901.dkr.ecr.us-east-2.amazonaws.com"


    }

    stages {
        stage('Build') {
            steps {

                sh '''
                cd polybot
                aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin $ECR_URL
                docker build -t edenb27-yolo5-app:0.0.$BUILD_NUMBER .
                docker tag edenb27-yolo5-app:0.0.$BUILD_NUMBER $ECR_URL/edenb27-yolo5-app:0.0.$BUILD_NUMBER
                docker push  $ECR_URL/edenb27-yolo5-app:0.0.$BUILD_NUMBER
                '''
            }
        }

        stage('Trigger Release') {
            steps {
                build job: 'Release', wait: false, parameters: [
                    string(name: 'IMG_URL', value: "$ECR_URL/edenb27-yolo5-app:0.0.$BUILD_NUMBER")
                ]
            }
        }
    }
}
