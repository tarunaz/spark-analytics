# Spark Sample

Read data from Apache Kafka topic, analyze data using Word2Vec model and publish the result to Kafka topic.

## Structure
- "requirement.txt": the python package needed for the script
- "build_config.yaml": the build configuration
- "image_stream.yaml": the image stream configuration
- "job.yaml": the job configuration 
- "../../spark/kafka_driver.py": the analytics script. Read data from kafka and process data in Spark

## Quick start

1. Install app requirements
   ```bash
   pip install -r requirement.txt
   ```

1. [Setup Apache Kafka](https://kafka.apache.org/documentation.html#quickstart)

1. Run the app
   ```bash
   python app.py
   ```

## Start on Openshift

1. Create new project
   ```bash
   oc new-project <project_name> --description="<description>"
   ```

1. Install and setup Oshinko
   ```bash
   oc create -f https://radanalytics.io/resources.yaml
   ```

1. Create Oshinko Cluster
   ```bash
   oc new-app oshinko-webui
   ```

1. Install apache kafka
   ```bash
   oc create -f https://raw.githubusercontent.com/mattf/openshift-kafka/master/resources.yaml
   oc new-app apache-kafka
   ```
   
1. If arguments change, update an configuration file (Optional)
   ```bash
   The following fields can be updated if arguments changes:
   - File "job.yaml" field "spec.template.spec.containers.env.APP_ARGS"
     - input_channel: This value should be Kafka, if using apache Kafka. Otherwise, could use File.
     - input_topic: the kafka topic to read data from.
     - output_topic: the kafka topic to publish result.
     - servers: the kafka brokers.
   - File "job.yaml" field "spec.template.spec.containers.env.OSHINKO_CLUSTER_NAME"
     use oc get po to check the oshinko cluster name.
   ```

1. Add the configuration file to Openshift
   ```bash
   oc create -f build_config.yaml
   oc create -f image_stream.yaml
   oc create -f job.yaml
   ```
   