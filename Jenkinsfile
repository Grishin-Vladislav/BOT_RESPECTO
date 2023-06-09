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
                             string(credentialsId: 'OPENAI_API_KEY', variable: 'OPENAI_API_KEY'),
                             string(credentialsId: 'DB_ROLE', variable: 'DB_ROLE'),
                             string(credentialsId: 'DB_PASSWORD', variable: 'DB_PASSWORD'),
                             string(credentialsId: 'PGADMIN_DEFAULT_EMAIL', variable:'PGADMIN_DEFAULT_EMAIL'),
                             string(credentialsId: 'PGADMIN_DEFAULT_PASSWORD', variable:'PGADMIN_DEFAULT_PASSWORD')
            ]){
                sh "docker-compose down || true \
                && docker-compose up --build -d"
            }
        }
    }
  }
}