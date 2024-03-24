pipeline {
    agent any

    parameters { string(name: 'POLYBOT_PROD_IMG_URL', defaultValue: '', description: '') }

    stages {
        stage('Update YAML') {
            steps {

                sh '''
                sed -i 's/image: .*/image: POLYBOT_PROD_IMG_URL/g' k8s/prod/polybot.yaml
                git checkout releases
                git merge master
                git add k8s/prod/polybot.yaml
                git commit -m "POLYBOT_PROD_IMG_URL"
                git push origin releases
                '''
            }
        }
    }
}
