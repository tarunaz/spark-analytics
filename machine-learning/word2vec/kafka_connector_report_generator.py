import os
import json

from pyspark import streaming
from kafka import KafkaConsumer

from datetime import datetime
from elasticsearch import Elasticsearch
from pyspark.ml.feature import Word2VecModel
from helper_method_lib import helper_method_process_data



class KafkaConnectorReportGenerator():
     """ A class that connect Spark with Kafka and builds reports with pre-built Word2Vec model. 

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
        model_date: the date of which model will be used

    """
    
    
     def __init__(self, servers, duration, spark_context, sql_context, model_save_path, model_date):
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
        self.model_date = model_date
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
        
        
     def configure_processing(self):
        """ A function to operate on input raw data generates report in desired format. 
        
        """
        # Load report making data
        print "============ NLP methods starts on report data ==================="
        df = helper_method_process_data(self.total_data, self.spark_context, self.sql_context)
        print "============ NLP methods finished on report data ==================="
        
        # load pre-generated model
        print "============= Loading pre-build model ======================="
        model_path = self.model_save_path + self.model_date + "/"
        model = Word2VecModel.load(model_path)
        print "====================== Model loading completed =============="

        report_data = df.rdd.map(lambda a:a.asDict()).collect()
        df.unpersist()
        del df
        
        ### report the result
        count_id = 1
        self.es = Elasticsearch([{'host': self.es_output_host, 'port': self.es_output_port }])
        
        print "============ Report seeding to Elastic Search start ===========" 
        output_index_name = self.es_output_index + '-' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        print "============ Result will be pushed in index:", output_index_name,"=============="
        
        for one_line_report in report_data:
            if len(one_line_report['features']) < 3:
                continue
           
            for word2vec_keyword in list(set(one_line_report['features'])):
                try:
                    synonyms = model.findSynonyms(word2vec_keyword, 10)
                    
                    self.send_result_to_elasticsearch(word2vec_keyword, synonyms, count_id, output_index_name)
                    count_id = count_id + 1  
                except Exception as e:
                    '''
                    It will come here if model did not get the current word'''
                    print e.message
                    pass
        print "================== Report seeding Ended============="
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
        
        self.consumer = KafkaConsumer(self.input_topic,
                                      bootstrap_servers=[self.servers],
                                      auto_offset_reset='earliest',
                                      consumer_timeout_ms=100000)

        self.total_data = []

        for msg in self.consumer:
            self.total_data.append(json.loads(msg.value))
            
        print "======Length of Total Data=========", len(self.total_data)
        #print "Taking only 30000 logs for testing purpose"
        #self.total_data = self.total_data[-30000:]
            
     def send_result_to_elasticsearch(self, word2vec_keyword, synonyms, count_id, output_index_name):
        """ Publish the word2vec data model results to elasticsearch
        
        Keyword arguments:
        word2vec_keyword -- the keyword generated by word2vec model
        synonyms -- a list of ten words that are similiar to keyword
        count_id -- the elasticsearch id for the entry

        """
        body = dict()
        body['Keywords'] = word2vec_keyword
        body['Result'] = dict()

        count = 0
        for word, cosine_distance in synonyms.collect():
            count = count + 1
            body['Result']['synonym_' + str(count)] = word

        self.es.index(index=output_index_name, doc_type='log', id=count_id, body=body)
    
