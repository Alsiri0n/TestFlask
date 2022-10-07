pipeline {
    agent {label "ubuntu"}

    stages {
        stage('SCM Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: scm.branches,
                    doGenerateSubmoduleConfigurations: true,
                    extensions: scm.extensions + [[$class: 'SubmoduleOption', parentCredentials: true]],
                    userRemoteConfigs: scm.userRemoteConfigs
                ])
                sh 'sudo cp -rvf * /root/floko3'
            }
        }
        stage('Build') {
            steps {
                sh 'sudo docker-compose -f /root/floko3/docker-compose.yml build'
            }
        }
        stage('Deploy') {
            steps {
                sh 'sudo HOST=$FLASK_HOST PORT=$FLASK_PORT docker-compose -f /root/floko3/docker-compose.yml up -d'
            }
        }
    }
}
