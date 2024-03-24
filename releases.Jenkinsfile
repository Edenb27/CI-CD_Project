pipeline {
    agent any

    parameters { string(name: 'POLYBOT_PROD_IMG_URL', defaultValue: '', description: '') }

    stages {
        stage('Update YAML') {
            steps {

                sh '''
                git checkout releases
                git merge origin/master
                sed -i 's/image: .*/image: POLYBOT_PROD_IMG_URL/g' k8s/prod/polybot.yaml

                git add k8s/prod/polybot.yaml
                git commit -c user.name='edenb27' -c user.email=edenblavat@gmail.com -m "POLYBOT_PROD_IMG_URL"
                git push origin releases
                '''
            }
        }
    }
}
