pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                echo currentBuild.description
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
