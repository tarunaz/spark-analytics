FROM radanalyticsio/openshift-spark:2.2-latest

USER root

RUN yum -y install epel-release
#Install pip for installing python libraries
RUN yum -y install python-pip

#Install the NLTK library for Spark
RUN pip install nltk

RUN export NLTK_DATA=/usr/share/nltk_data

#The NLTK library needs a language, this installs punkt
RUN python -m nltk.downloader -d /usr/share/nltk_data punkt

RUN chmod 0755 /usr/share/nltk_data

USER 1000

#Install hadoop-aws-2.7.3 jar
RUN wget http://central.maven.org/maven2/org/apache/hadoop/hadoop-aws/2.7.3/hadoop-aws-2.7.3.jar -O /opt/spark/jars/hadoop-aws-2.7.3.jar
#Install aws=java-sdk-1.7.4.jar
RUN wget http://central.maven.org/maven2/com/amazonaws/aws-java-sdk/1.7.4/aws-java-sdk-1.7.4.jar -O /opt/spark/jars/aws-java-sdk-1.7.4.jar

#CMD ["/usr/local/s2i/usage"]
