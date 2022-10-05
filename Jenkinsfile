pipeline {
    agent {label "ubuntu"}
    environment {
        EXAMPLE_CREDS=credentials('flask-host')
    }

    stages {
        stage('SCM Checkout') {
            steps {
                echo $flask-host
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
