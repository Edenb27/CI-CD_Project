pipeline {
    agent any

    parameters { string(name: 'IMG_URL', defaultValue: '', description: '') }

    stages {
        stage('Update YAML') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'github', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh '''

                    printenv

                    if [[ $IMG_URL == *"-polybot-"* ]]; then
                      YAML_FILE="k8s/prod/polybot.yaml"
                    elif [[ $IMG_URL == *"-yolo5-"* ]]; then
                      YAML_FILE="k8s/prod/yolo5.yaml"
                    else
                        exit 7
                    fi

                    git config --global user.email "edenblavat@gmail.com"
                    git config --global user.name "edenb27"

                    git checkout releases
                    git pull origin releases
                    git merge origin/master
                    sed -i "s|image: .*|image: ${IMG_URL}|g" $YAML_FILE

                    git add $YAML_FILE
                    git commit -m "IMG_URL"
                    git push https://edenb27:$PASSWORD@github.com/Edenb27/CI-CD_Project.git releases
                    '''
                }
            }
        }
    }
}
