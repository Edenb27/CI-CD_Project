pipeline {
    agent {
        docker {
            label 'general'
            image '352708296901.dkr.ecr.us-east-2.amazonaws.com/edenb27-polybot-app:V1.0.24'
            args  '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        ECR_URL = "352708296901.dkr.ecr.us-east-2.amazonaws.com"

    }

    stages {
        stage('Build') {
            steps {
                sh '''
                pwd
                aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin $ECR_URL
                docker build -t $ECR_URL/edenb27-polybot-app:0.0.2 .
                docker push $ECR_URL/edenb27-jenkins:0.0.2
                '''
            }
            post {
                always {
                    sh 'docker image prune -a --force'
                }
            }
        }

//         stage('Trigger Deploy') {
//             steps {
//                 build job: 'RobertaDeploy', wait: false, parameters: [
//                     string(name: 'ROBERTA_IMAGE_URL', value: '$ECR_URL/edenb27-jenkins:0.0.4')
//                 ]
//             }
//         }
//     }
}