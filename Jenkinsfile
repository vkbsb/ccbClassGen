#!/usr/bin/env groovy

String version = "1.2.3"

node {       
    echo 'Building..'
    def changeLogSets = currentBuild.changeSets                
    for (int i = 0; i < changeLogSets.size(); i++) {
        def entries = changeLogSets[i].items
        for (int j = 0; j < entries.length; j++) {
            def entry = entries[j]
            echo "${entry.commitId} by ${entry.author} on ${new Date(entry.timestamp)}: ${entry.msg}"
        }
    }

    echo 'Deploying....'
    def response = httpRequest "http://httpbin.org/response-headers?param1=$version"
    println( response )
}
