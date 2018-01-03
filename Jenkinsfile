pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                echo $description
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
