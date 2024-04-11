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
                docker build -t edenb27-polybot-app:0.0.$BUILD_NUMBER .
                docker tag $IMAGE_NAME_POLYBOT:0.0.edenb27-polybot-app $ECR_URL/edenb27-polybot-app:0.0.$BUILD_NUMBER
                docker push  $ECR_URL/edenb27-polybot-app:0.0.$BUILD_NUMBE
                echo test
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
                    string(name: 'IMG_URL', value: '$ECR_URL/edenb27-polybot-app:0.0.$BUILD_NUMBER')
                ]
            }
        }
    }
}
