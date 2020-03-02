pipeline {
    agent {
      dockerfile  {
        filename 'Dockerfile'
      }
    }
  stages {
    stage("Set secrets"){
        steps {
          script{

          def secrets = [
                  [path: 'infra/grafana', engineVersion: 1, secretValues: [
                                                  [envVar: 'GRAFANA_API_KEY', vaultKey: 'api_key']]],
                 [path: 'infra/grafana', engineVersion: 1, secretValues: [
                                                  [envVar: 'GRAFANA_HOST', vaultKey: 'host']]],
                  [path: 'infra/grafana', engineVersion: 1, secretValues: [
                                                  [envVar: 'GRAFANA_PROTOCOL', vaultKey: 'protocol']]],
              ]

          def configuration = [vaultUrl: 'https://vault-stage.grofer.io',vaultCredentialId: 'jenkins-vault-token',
                                                engineVersion: 1]

          withVault([configuration: configuration, vaultSecrets: secrets]) {
                  sh '''
                    chmod u+x test.sh 
                    ./test.sh
                  '''
          }
        }
      }
    }
    stage("Running yaml linter"){
      steps {
        sh '''
          yamllint  -d relaxed .
          # All files added for yaml lint check
          '''
      }
    }
    // stage("Running pylint"){
    //   steps{
    //     sh '''
    //       pylint .
    //     '''
    //   }
    // }
  }
}