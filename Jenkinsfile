pipeline {
        agent any
        stages {
            stage('Build') {
                steps {
                    // Your build steps here
                    sh 'echo "Building..."'
                    // Send build information to Jira
                    jiraSendBuildInfo(site: 'palbuquerque.atlassian.net', branch: 'DFM-7-Jenkins-branch')
                }
            }
            stage('Deploy') {
                steps {
                    // Your deployment steps here
                    sh 'echo "Deploying..."'
                    // Send deployment information to Jira
                    jiraSendDeploymentInfo(site: 'palbuquerque.atlassian.net', branch: 'DFM-7-Jenkins-branch')
                }
            }
        }
    }
