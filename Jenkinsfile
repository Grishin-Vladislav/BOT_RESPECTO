properties([pipelineTriggers([githubPush()])])

pipeline {
  agent any
  stages {
    stage('Checkout SCM') {
            steps {
                checkout([
                 $class: 'GitSCM',
                 branches: [[name: 'ci-cd']],
                 userRemoteConfigs: [[
                    url: 'git@github.com:frodan/BOT_RESPECTO.git',
                    credentialsId: '',
                 ]]
                ])
            }
        }


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
                && docker run --init -d --name bot_respect -e {env.TG_API_KEY} -e {env.OPENAI_API_KEY} frodan/bot_respect'
            }
        }
    }
  }
}