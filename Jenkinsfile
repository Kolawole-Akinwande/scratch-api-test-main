pipeline {
    agent  any 
    environment {
        COMMIT = sh(returnStdout: true, script: "git rev-parse HEAD").trim()
        TAG = "${env.BRANCH_NAME == 'master' ? 'production' : 'dev'}-${env.COMMIT}"
        ENVIRONMENT = "${env.BRANCH_NAME == 'master' ? 'staging' : 'development'}"
    }

    stages {
        stage('build-test'){
            parallel {
                stage('build') {
                    // when{
                    //     changeset "**/cidr_convert_api/python/**"
                    // }
                    steps {
                        
                        echo "Building docker image ${TAG}"
                        sh 'docker build -t kolsdej/scratch-api-test:${TAG} .'

                    }
                    post {
                        success {
                            echo '\u2705 Build Succeeded, pushing image to registry...'
                            sh 'docker push kolsdej/scratch-api-test:${TAG}'
                            sh 'docker rmi kolsdej/scratch-api-test:${TAG}'
                            
                        }
                        failure {
                            echo 'Build Failed \u274C'
                        }
                    }
                }
                stage('test') {
                    agent {docker {
                        image 'kolsdej/scratch-api-test:latest'
                        args '-v /tmp:/tmp'
                        }
                    }
                    steps {
                        sh 'python -m unittest discover scratch/tests'
                        withEnv(['PYLINTHOME=.']) {
                            sh "pylint --output-format=parseable --exit-zero  --reports=no *.py"
                        }
                    }
                    post {
                        success {
                            echo '\u2705 ...Test passed...'
                        }
                        failure {
                            echo '\u274C ...Test Failed...'
                        }
                    }
                }
            }
        }
        
        stage('deploy') {
            parallel {
                stage('development'){
                    when{
                        expression {env.ENVIRONMENT == 'development'}
                    }
                    steps {
                        kubeDeploy(environment: "${env.ENVIRONMENT}")
                    }
                    post {
                        success {
                            echo " \u2705 Successfully Deployed to ${ENVIRONMENT}"
                        }
                        failure {
                            echo " \u274C Deployment to ${ENVIRONMENT} failed"
                            kubeRollback(environment: "${env.ENVIRONMENT}")
                        }
                    }
                }
                stage('staging'){
                    when {
                        expression {env.ENVIRONMENT == 'staging'}
                    }
                    steps {
                        kubeDeploy(environment: "${env.ENVIRONMENT}")
                    }
                    post {
                        success {
                            echo "\u2705 Successfully Deployed to ${ENVIRONMENT}"
                            script {
                                if (env.ENVIRONMENT == "staging") {
                                    env.PRODUCTION = 'production'
                                }
                            }
                        }
                        failure {
                            echo " \u274C Deployment to ${ENVIRONMENT} failed"
                            kubeRollback(environment: "${env.ENVIRONMENT}")
                        }
                    }

                }
            }
            
        }
        stage ('production') {
            when {
                    expression {env.PRODUCTION == 'production'}
                }
            steps {
                withCredentials([usernamePassword(credentialsId: 'github_cred', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                    sh "git tag ${TAG}"
                    sh "git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/Kolawole-Akinwande/scratch-api-test-main.git ${TAG}"
                }
                kubeDeploy(environment: "${env.PRODUCTION}")
            }
            post {
                success {
                    echo "\u2705 Successfully Deployed to ${PRODUCTION}"
                }
                failure {
                    echo " \u2705 Deployment to ${PRODUCTION} failed. rolling back..."
                    kubeRollback(environment: "${env.PRODUCTION}")
                }
            }
        }
    }
}
def kubeDeploy(Map map) {
    withCredentials([file(credentialsId: 'KUBECONFIG2', variable: 'KUBECONFIG')]) {
        // some block
        sh "kubectl --kubeconfig=${KUBECONFIG} --namespace=default set image deployment/scratch-api-test scratch-api-test=kolsdej/scratch-api-test:${TAG}"
        sh "kubectl --kubeconfig=${KUBECONFIG} --namespace=default rollout status deployment/scratch-api-test --timeout=120s"
        echo "Deployed to ${map.environment}"
    }
        
}

def kubeRollback(Map map) {
    withCredentials([file(credentialsId: 'KUBECONFIG2', variable: 'KUBECONFIG')]) {
        sh "kubectl --kubeconfig=${KUBECONFIG} --namespace=default rollout undo deployment/scratch-api-test"
    }
}