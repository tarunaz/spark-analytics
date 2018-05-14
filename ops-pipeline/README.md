## Folder Structure

- es-to-kafka-model-building-nightly: include a Jenkinsfile that checkouts container-logstash git repo. Then pulling the data from elasticsearch to kafka based on provided query. The process will run everyday at 11pm EST. The pulled data will be used to construct data model. The data model will be stored in model/suhojit in openshift oshinko worker cluster.
> Jenkins job link: https://jenkins-dh-ci.ose.sbu.lab.eng.bos.redhat.com/job/playbook-trigger-nightly/

- es-to-kafka-model-running-nightly: include a Jenkinsfile that checkouts container-logstash git repo. Then pulling the data from elasticsearch to kafka based on provided query. The process will run everyday at 11pm EST. The data will be analyzed with data model stored in model/suhojit in openshift oshinko worker cluster.
> Jenkins job link: https://jenkins-dh-ci.ose.sbu.lab.eng.bos.redhat.com/job/playbook-trigger-model-running-nightly/


## Deployment of Jenkinsfile

Jenkinsfile doesn't create Jenkins job. Instead, user needs to create a Jenkins pipeline job first, and then links Jenkinsfile to that job through "Pipeline" field in Jenkins job configuration.
