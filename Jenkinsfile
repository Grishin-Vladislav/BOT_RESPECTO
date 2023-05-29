properties([pipelineTriggers([githubPush()])])

pipeline {
  agent any
  stages {
    stage('Docker Build') {
      agent any
      steps {
        sh 'docker build . --file Dockerfile --tag frodan/bot_respect'
      }
    }
    stage('Deploy'){
        agent any
        steps{
            withCredentials([string(credentialsId: 'TG_API_KEY', variable: 'TG_API_KEY'),
                             string(credentialsId: 'OPENAI_API_KEY', variable: 'OPENAI_API_KEY')
            ]){
                sh 'docker stop bot_respect || true \
                && docker rm bot_respect || true \
                && docker run --name bot_respect -e TELEGRAM_API_KEY=${env.TG_API_KEY} -e OPENAI_API_KEY=${env.OPENAI_API_KEY} frodan/bot_respect'
            }
        }
    }
  }
}