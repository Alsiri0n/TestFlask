pipeline {
    agent {label "ubuntu"}
    environment {
        FLASK_HOST = credentials('flask-host')
        FLASK_PORT = credentials('flask-port')
    }

    stages {
        stage('SCM Checkout') {
            steps {
                sh 'echo $EXAMPLE_CREDS'
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
                sh 'sudo docker-compose -f /root/floko3/docker-compose.yml up -d'
            }
        }
    }
}
