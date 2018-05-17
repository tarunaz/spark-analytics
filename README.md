## spark-analytics

This folder contains information for deploying and running analytics job.

## Folder Structure

- ansible/: spark oshinko cluster deployment
- configs/openshift: configuration file for bc, is, and job
- experimental/: store any analytics sccripts that are still in progress
- machine-learning/: store all machine learning algorithms in use
- ops-pipeline/: Jenkinsfile to kick off job

## Usage

- docker build -f Dockerfile_spark_cluster_image -t spark-analytics:2.3.0 .
- docker tag <imageid> tmehrarh/spark-analytics:2.3.0
- docker push tmehrarh/spark-analytics:2.3.0
