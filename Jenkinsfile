pipeline {

  environment {
    PROJECT = "demo2-248908"
    APP_NAME = "cfgmanapp"
    IMAGE_TAG = "eu.gcr.io/${PROJECT}/${APP_NAME}:${GIT_COMMIT}"
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
  - name: jenkins-gcr-sa-creds
    secret:
      secretName: jenkins-gcr-json
  containers:
  - name: git
    image: gcr.io/cloud-builders/git
    command:
    - cat
    tty: true
  - name: python
    image: gcr.io/cloud-marketplace/google/python
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
    - name: jenkins-gcr-sa-creds
      mountPath: /tmp/gcr/
      readOnly: true
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
        }
    } 
} 
        stage('Push container') {
      steps {
        container('docker') {
          sh "cat /tmp/gcr/jenkins-gcr.json | docker login -u _json_key --password-stdin https://eu.gcr.io";
          sh "docker push ${IMAGE_TAG}";
			// script {
      //       docker.withRegistry("https://eu.gcr.io", "gcr:${STORAGE_CREDS}") {
      //       sh "docker push ${IMAGE_TAG}"
			//      }
      //   }
    }}}
        stage('Deploy') {
      steps {
        container('kubectl') {
	 sh """sed -i "s/CONTAINERTAG/${GIT_COMMIT}/g" deployment_dev """
         sh """sed -i "s/PROJECTID/${PROJECT}/g" deployment_dev """
         sh "kubectl apply -f deployment_dev"
       //  sh "kubectl create deployment ConfigManager --image=${IMAGE_TAG}";
        // sh "kubectl get pods";
        // sh "kubectl expose deployment ConfigManager --type=LoadBalancer --port 80 --target-port 5004";
        }
    } 
}

}
}
