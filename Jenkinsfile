pipeline {
    environment {
        VERSION = getVersion()
        DOCKER_VERSION = getDockerVersion()
        registryCredential = 'docker-hub'
    }
    agent {
        docker {
            image 'python:3.9.5'
            args '-u root'
        }
    } 

    stages {
        stage('build') {
            steps {
                sh 'pip install --no-cache-dir -r requirements.txt'
            }
        }
        stage('build docker') {
            steps {
                        docker.withRegistry('https://registry.hub.docker.com/v1/repositories/woped', registryCredential) {
                            def dockerImage = docker.build("woped/text2process-stanford:$DOCKER_VERSION")
                            def dockerImageLatest = docker.build("woped/text2process-stanford:latest")
                            dockerImage.push();
                            dockerImageLatest.push();
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            setBuildStatus("Build succeeded", "SUCCESS");
        }
        failure {
            setBuildStatus("Build not Successfull", "FAILURE");
            
            emailext body: "Something is wrong with ${env.BUILD_URL}",
                subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
                to: '${DEFAULT_RECIPIENTS}'
        }
    }
}

def getVersion() {
    return '0.1'
}

def getDockerVersion() {
    version = '0.1'

    if(version.toString().contains('SNAPSHOT')) {
        return version + '-' + "${currentBuild.startTimeInMillis}"
    } else {
        return version
    }
}

void setBuildStatus(String message, String state) {
  step([
      $class: "GitHubCommitStatusSetter",
      reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/tfreytag/woped-stanford-core-rest-service"],
      contextSource: [$class: "ManuallyEnteredCommitContextSource", context: "ci/jenkins/build-status"],
      errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
      statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]] ]
  ]);
}
