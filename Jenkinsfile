pipeline {
    agent any
    stages {
        stage("Running tests for dashboard") {
            agent {
                dockerfile {
                    filename 'Dockerfile'
                }
            }
            steps {
                script {
                    def secrets = [
                            [path: 'infra/legend/grafana', engineVersion: 1, secretValues: [
                                    [envVar: 'GRAFANA_API_KEY', vaultKey: 'api_key']]],
                            [path: 'infra/legend/grafana', engineVersion: 1, secretValues: [
                                    [envVar: 'GRAFANA_HOST', vaultKey: 'host']]],
                            [path: 'infra/legend/grafana', engineVersion: 1, secretValues: [
                                    [envVar: 'GRAFANA_PROTOCOL', vaultKey: 'protocol']]],
                    ]
                    def configuration = [vaultUrl: 'https://vault-stage.grofer.io', vaultCredentialId: 'jenkins-vault-token',
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
        stage("Image build and push to repo") {
            when {
                    branch "master"
            }
            steps {
                sh '''
            docker build -t registry.grofer.io/infra/legend/legend:latest .
            docker push registry.grofer.io/infra/legend/legend:latest
                '''
            }
        }
    }
}