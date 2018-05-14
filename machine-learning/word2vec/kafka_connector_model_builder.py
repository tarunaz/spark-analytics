import os
import json
import kafka
import string
import nltk

from pyspark import streaming
from kafka import KafkaConsumer
from pyspark.sql import Row
from pyspark.sql.functions import udf
from pyspark.sql import functions as func
from pyspark.sql.types import BooleanType, DoubleType
from pyspark.ml.feature import Word2Vec
from datetime import datetime

from helper_method_lib import helper_method_process_data



class KafkaConnectorModelBuilder():
     """ A class that connect Spark with Kafka and builds Word2Vec model. 

    This class wraps the Spark and Kafka specific logic for creating a
    DStream and applying processing functions to the RDDs contained
    therein.

    Attributes:
        input_topic: the kafka topic that the program read raw data from
        total_data: store all the raw data
        server: a list of Kafka brokers
        spark_context: main entry point for Spark functionality
        streaming_context: connection to the spark cluster
        kafka_stream: input stream that pulls message from Kafka
        model_save_path: location where model will be saved

    """
     def __init__(self, servers, duration, spark_context, sql_context, model_save_path):
        """ Create a KafakConnector object.

        Keyword arguments:
        servers -- A list of Kafka brokers
        duration -- The window duration to sample the Kafka stream in
                    seconds
        spark_context -- main entry point for Spark functionality
        sql_context -- The entry point for working with structured data
        """
        self.servers = servers
        self.spark_context = spark_context
        self.streaming_context = streaming.StreamingContext(
            self.spark_context, duration)
        self.sql_context = sql_context
        self.model_save_path = model_save_path
        self.es_output_host = os.environ.get('ES_HOST')
        self.es_output_port = os.environ.get('ES_PORT')
        self.es_output_index = os.environ.get('ES_OUTPUT_INDEX')
    
    
    
     def start_and_await_termination(self):
        """ Start the stream processor.

        This function will start the Spark-based stream processor,
        it will run until `stop` is called or an exception is
        thrown.

        """
        self.configure_processing()
        #self.streaming_context.start()
        #self.streaming_context.awaitTermination()        






     def helper_method_run_model(self, df):
        """ Build Word2Vec Model.
 
        Keyword arguments:
        df -- model input in data frame format
        
        """
        word2Vec = Word2Vec(vectorSize=100, seed=10, minCount=3, inputCol="features", outputCol="result")

        model = word2Vec.fit(df)

        print "\n\n =================== Model building completed ================== \n\n"
        df.unpersist()
        del df
        return model
    
     def configure_processing(self):
        """ A function to operate on input raw data. This method calls the data processor and model builder. 
        After model creation, it saves the model.
        
        """
        print "inside configure_processing KEYS:", self.total_data[0].keys()
        df = helper_method_process_data(self.total_data, self.spark_context, self.sql_context)
        
        print "\n Some rows from processed data.."
        df.head()

        model = self.helper_method_run_model(df)
        
        model_path = self.model_save_path + datetime.now().strftime("%Y-%m-%d") + "/"
        
        model.write().overwrite().save(model_path)
        print "\n\n =================== Model saving completed ================== \n\n"
        
     def stop(self):
        """Stop the stream processor."""

        self.streaming_context.stop()
        
        
     def create_kafka_data_stream(self, input_topic): 
        """ Create an input stream that pull message from a Kafka
        broker.
        
        Keyword arguments:
        input_topic -- Kafka topic to read messages from

        """
        self.input_topic = input_topic
        print "input_topic {}".format(input_topic)
        print "servers: {}".format(self.servers)
        
        self.consumer = KafkaConsumer(self.input_topic,
                                      bootstrap_servers=[self.servers],
                                      auto_offset_reset='earliest',
                                      consumer_timeout_ms=100000)

        self.total_data = []

        for msg in self.consumer:
            self.total_data.append(json.loads(msg.value))

        print "======Length of Total Data=========", len(self.total_data)
        print "inside create_kafka_data_stream KEYS:", self.total_data[0].keys()
        print "================Printing one record======================"
        print self.total_data[0]
        print "Taking only 30000 logs for testing purpose"
        self.total_data = self.total_data[:30000]
    
    
