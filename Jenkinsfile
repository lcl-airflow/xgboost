//TODO: fix variable, fix hard coded stuff!!! :)

pipeline {
    environment {
    //CREDENTIALS
    CREDENTIAL_ID = 'docker-hub-credentials'
    JENKINS_SERVICE_ACCOUNT_KEY='jenkins-k8'
    //GCP
    REGION='us-central1'
    PROJECT='lt-dia-playground-sb'


    //Docker Parameters
    REGISTRY = 'https://nexus-repo.[l0bl*w.ca].ca:8082'
    DOCKER_AGENT= 'nexus-repo.[l0bl*w.ca]:8082/dataeng-mlengine:0.2'
    DOCKER_IMG='dataeng-mlengine'
    DOCKER_VER='0.2'
    
    //BUILD model
    DATASOUCE='https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data'
    TESTSOURCE='https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test'
    

    //MODEL PARAMETERS Starts Here
    VERSION_NAME="v1"  //TODO:  AUTO_GENERATE VERSION #s
    MODEL_DIR='gs://ml-eng-model/'
    MODEL_NAME='Demo'
    FRAMEWORK= "XGBOOST"
    RUNTIME_VER='2.1'
    MACHINE='n1-standard-2'
    }

    agent {
       label 'BUILD_AGENT_UNIX'
    }

    stages{
        stage('Build Image'){
                steps{
                    script {
                        withCredentials([usernamePassword( credentialsId: "${CREDENTIAL_ID}" , usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                        docker.withRegistry( "${REGISTRY}"  , "${CREDENTIAL_ID}" ) {
                        image_2 = docker.build "'${DOCKER_IMG}':'${DOCKER_VER}'"
                        image_2.push()
                        }
                }  
                }
            
            }
        }
        //TODO:  Train the model in AI-platform @ Scale
        stage('Train Model') {
            agent {
                docker { 
                    image 'nexus-repo.[l0bl*w.ca].ca:8082/dataeng-mlengine:0.2'
                    reuseNode true
                }
            }
            steps {
                sh 'rm -Rf ml_engine/census_data/'
                sh 'mkdir ml_engine/census_data/'
                sh("curl '${DATASOUCE}' -o ./ml_engine/census_data/adult.data")
                sh("curl '${TESTSOURCE}' -o ./ml_engine/census_data/adult.test")
                sh 'ls -larth ml_engine/census_data/'   
                sh 'python ml_engine/main.py'
                sh 'ls -larth ml_engine/'
            }
        }
        stage('Push Model to GCS') {
            steps {
                withCredentials([file(credentialsId: "${JENKINS_SERVICE_ACCOUNT_KEY}" , variable: 'GC_KEY')]) {
                    sh("gcloud auth activate-service-account --key-file='${GC_KEY}'")
                    sh("gsutil cp ml_engine/model.joblib gs://ml-eng-model/")
                    sh('gsutil ls gs://ml-eng-model')
                }
            }
        }    
        stage('Create Model on AI Platform') {
            steps {
                withCredentials([file(credentialsId: "${JENKINS_SERVICE_ACCOUNT_KEY}" , variable: 'GC_KEY')]) {
                    sh("gcloud auth activate-service-account --key-file='${GC_KEY}'")
                    sh("gcloud config set project '${PROJECT}'")
                   // sh ("gcloud ai-platform models delete '${MODEL_NAME}'")
                    sh ("gcloud ai-platform models create '${MODEL_NAME}' --description=opsengdemo --enable-logging --regions='${REGION}'")
                }
            }
        }    
        stage('Add New Version') {
            //TODO:  GOOGLE SDK needs to be updated in JENKINS.   have tried using docker agent but during authenthication it generates permissions error.   Looks like is a bug
            steps {
                withCredentials([file(credentialsId: "${JENKINS_SERVICE_ACCOUNT_KEY}" , variable: 'GC_KEY')]) {
                    sh("gcloud auth activate-service-account --key-file='${GC_KEY}'")
                    sh("gcloud config set project '${PROJECT}'")
                    sh("gcloud ai-platform versions create '${VERSION_NAME}' --model '${MODEL_NAME}' --origin '${MODEL_DIR}' --runtime-version '${RUNTIME_VER}' --framework '${FRAMEWORK}' --python-version 3.7")
                }
            }
        } 
    
        stage('Test Model') {
            steps {
                withCredentials([file(credentialsId: "${JENKINS_SERVICE_ACCOUNT_KEY}" , variable: 'GC_KEY')]) {
                  sh("gcloud --quiet auth activate-service-account --key-file='${GC_KEY}'")
                   sh("gcloud config set project '${PROJECT}'")

                }
            }
        }  
}
}
