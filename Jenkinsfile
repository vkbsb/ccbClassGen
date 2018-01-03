#!/usr/bin/env groovy


def tryHttpRequest(){
    String version = "1.2.3"
    def response = httpRequest "http://httpbin.org/response-headers?param1=$version"
    println( response )
}

node {       
    stage('Clone sources') {
        git url: 'https://github.com/vkbsb/ccbClassGen.git'
    }

    stage('Build') {
        if (env.BRANCH_NAME == 'master') {
            echo 'I only execute on the master branch'
            def changeLogSets = currentBuild.changeSets
            println("changeLogSets: ${changeLogSets.size()}")                
            for (int i = 0; i < changeLogSets.size(); i++) {
                def entries = changeLogSets[i].items
                for (int j = 0; j < entries.length; j++) {
                    def entry = entries[j]
                    echo "${entry.commitId} by ${entry.author} on ${new Date(entry.timestamp)}: ${entry.msg}"
                }
            }
        } else {
            echo 'I execute elsewhere'
        }
    }

    stage('Deploy'){
        tryHttpRequest()
    }
}
