pipeline {
    agent any


    environment {
        ECR_URL = "352708296901.dkr.ecr.us-east-2.amazonaws.com"
        IMAGE_NAME_POLYBOT = "edenb27-polybot-app"

    }

    stages {
        stage('Build') {
            steps {

                sh '''
                cd polybot
                aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin $ECR_URL
                docker build -t $IMAGE_NAME_POLYBOT:0.0.$BUILD_NUMBER .
                docker tag $IMAGE_NAME_POLYBOT:0.0.$BUILD_NUMBER $ECR_URL/IMAGE_NAME_POLYBOT:0.0.$BUILD_NUMBER
                docker push  $ECR_URL/IMAGE_NAME_POLYBOT:0.0.$BUILD_NUMBER
                '''
            }
            post {
                always {
                    sh 'docker image prune -a --force'
                }
            }
        }

        stage('Trigger Release') {
            steps {
                build job: 'Release', wait: false, parameters: [
                    string(name: 'IMG_URL', value: '$ECR_URL/$IMAGE_NAME:0.0.$BUILD_NUMBER')
                ]
            }
        }
    }
}
