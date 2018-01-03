pipeline {
    agent any
    def changeLogSets
    def version
    def response

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                changeSets = currentBuild.changeSets                
                for (int i = 0; i < changeLogSets.size(); i++) {
                    def entries = changeLogSets[i].items
                    for (int j = 0; j < entries.length; j++) {
                        def entry = entries[j]
                        echo "${entry.commitId} by ${entry.author} on ${new Date(entry.timestamp)}: ${entry.msg}"
                    }
                }
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
                version = "1.2.3"
                response = httpRequest "http://httpbin.org/response-headers?param1=$version"
                println( response )
            }
        }
    }
}
