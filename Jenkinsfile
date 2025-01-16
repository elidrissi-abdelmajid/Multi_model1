pipelines{
    agnt any
    stages{
        stage("clone the repository"){
            steps{
                script{
                    branch "master", url "git@github.com:elidrissi-abdelmajid/Multi_model1.git"
                }
            }
        }
        stage("Build the image"){
            steps{
                script{
                    bat "docker build -t ${IMAGE_DOCKER}:${TAG} . "
                }
            }
        }
        stage ("login to docker hub"){
            steps{
                script{
                    bat "docker login -u ${USER_NAME} -p ${TOKEN}"
                }
            }
        }
         stage ("Push the image"){
            steps{
                script{
                    bat "docker push ${USER_NAME}/${IMAGE_DOCKER}:${TAG}"
                }
            }
        }
    }
}