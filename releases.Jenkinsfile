pipeline {
    agent any

    parameters { string(name: 'POLYBOT_PROD_IMG_URL', defaultValue: '', description: '') }

    stages {
        stage('Update YAML') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'github', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh '''
                    git checkout releases
                    git -c user.name='edenb27' -c user.email=edenblavat@gmail.com merge origin/master
                    sed -i "s|image: .*|image: ${POLYBOT_PROD_IMG_URL}|g" k8s/prod/polybot.yaml

                    git add k8s/prod/polybot.yaml
                    git -c user.name='edenb27' -c user.email=edenblavat@gmail.com commit -m "POLYBOT_PROD_IMG_URL"
                    git push https://edenb27:$PASSWORD@github.com/Edenb27/CI-CD_Project.git releases
                    '''
                }
            }
        }
    }
}
