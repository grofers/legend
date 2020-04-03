pipeline {
    agent {
      dockerfile  {
        filename 'Dockerfile'
      }
    }
  stages {
    stage("Running tests for dashboard"){
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
                    cd tests
                    chmod u+x tests.sh
                    ./tests.sh
                  '''
          }
        }
      }
    }
  }
}