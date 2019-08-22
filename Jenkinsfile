pipeline {

  environment {
    PROJECT = "demo2-248908"
    APP_NAME = "cfgmanapp"
    FE_SVC_NAME = "${APP_NAME}-backend"
    CLUSTER = "demo2-gke-cluster"
    CLUSTER_ZONE = "europe-west3-a"
    IMAGE_TAG = "eu.gcr.io/${PROJECT}/${APP_NAME}:${env.BUILD_NUMBER}"
    JENKINS_CRED = "${PROJECT}"
    BUILD_HOME='/var/lib/jenkins/workspace'
    APP_REPO="https://github.com/kv-053-devops/cfgmanapp.git"
  }

 agent {
    kubernetes {
    //   label 'ConfigManager'
    //   defaultContainer 'jnlp'
      yaml """
apiVersion: v1
kind: Pod
metadata:
labels:
  component: ci
spec:
  # Use service account that can deploy to all namespaces
  serviceAccountName: jenkins-sa
  volumes:
  - name: dockersock
    hostPath:
      path: /var/run/docker.sock
  containers:
  - name: git
    image: gcr.io/cloud-builders/git
    command:
    - cat
    tty: true
  - name: docker
    image: gcr.io/cloud-builders/docker
    command:
    - cat
    tty: true
    volumeMounts:
    - name: dockersock
      mountPath: /var/run/docker.sock
  - name: kubectl
    image: gcr.io/cloud-builders/kubectl
    command:
    - cat
    tty: true
"""
}
  }
  stages {
    stage('Checkout') {
        steps {
            git branch: 'master', url: "${APP_REPO}"
        }
    }
    stage('Build and push container') {
      steps {
        container('docker') {
        //  sh "cd $WORKSPACE/repo/${APP_NAME}";
         sh "docker build -t ${IMAGE_TAG} .";
         sh "docker images";
        }
    } 
} 
        stage('Push container') {
      steps {
        container('docker') {
			script {
            docker.withRegistry("https://eu.gcr.io", "gcr:cfgmanapp") {
            sh "docker push ${IMAGE_TAG}"
			}
        }
    }}}
        stage('Deploy') {
      steps {
        container('kubectl') {
         sh "kubectl create deployment ConfigManager --image=${IMAGE_TAG}";
         sh "kubectl get pods";
         sh "kubectl expose deployment ConfigManager --type=LoadBalancer --port 80 --target-port 5004";
        }
    } 
}

}
}
