import timeit
import os
import sys
import nltk

from pyspark import SparkContext, SparkConf
from pyspark import HiveContext
from argparse import ArgumentParser

from kafka_connector_model_builder import KafkaConnectorModelBuilder
from kafka_connector_report_generator import KafkaConnectorReportGenerator



#es = Elasticsearch([{'host': 'elasticsearch.perf.lab.eng.bos.redhat.com', 'port': 80}])

### Create the Spark contexts
start_timer = timeit.default_timer()

print "Creating the Spark Context..."
#os.environ["SPARK_HOME"] = "/home/submukhe/App/spark"
#conf = (SparkConf().setMaster("local[*]")
#            .setAppName("Word2Vec"))

### Custom settings for Spark contexts

#SparkContext.setSystemProperty('spark.driver.memory', '4g')
#SparkContext.setSystemProperty('spark.executor.memory', '3g')
SparkContext.setSystemProperty('spark.sql.tungsten.enabled', 'true')

conf = (SparkConf().setAppName("Word2Vec"))

sc = SparkContext(conf = conf)
sqlContext = HiveContext(sc)

print "======== Some useful Spark configs:============"

for elem in sc._conf.getAll():
    print "\nKey:", str(elem[0])," Value:", str(elem[1])
    print "--------------------------------------------------------"




def parse_args():
    '''
    This method will take inputs from commandline.
    
    '''
    parser = ArgumentParser(description='Input, Output, Model Saving Path, Model Date, Servers and Input-Output topic')
    parser.add_argument('-c', '--channel',
                        help='output channel of word2vec model result. The parameter, -c, can be either ELK or Excel.'
    )
    parser.add_argument('--input_channel', help ='input channel. it can be either File or Kafka')
    parser.add_argument('--operation_type', help = 'either model_builder or report_generator')
    parser.add_argument('--input_topic',
        help='the kafka topic to read data from')
    parser.add_argument('--servers', help='the kafka brokers')
    parser.add_argument('--model_date', help='the date of which model will be used ')
    parser.add_argument('--model_save_path', help='the path from where model is to be loaded or saved')
    
    return parser.parse_args()

args = parse_args()


input_channel = args.input_channel
operation_type = args.operation_type

if input_channel == 'Kafka':
    if operation_type == 'model_builder':
        kc = KafkaConnectorModelBuilder(args.servers, 180, sc, sqlContext, args.model_save_path)
        kc.create_kafka_data_stream(args.input_topic)
        kc.start_and_await_termination()
        
    elif operation_type == 'report_generator':
        kc = KafkaConnectorReportGenerator(args.servers, 180, sc, sqlContext, args.model_save_path, args.model_date)
        kc.create_kafka_data_stream(args.input_topic)
        kc.start_and_await_termination()
        
    else:
        print "operation_type is necessary"
        sys.exit(1)
        
else:
    print "This module supports Kafka type of input channel only"
    sys.exit(1)
    
    
print "Total time taken for ",args.operation_type, " is:", (timeit.default_number - start_timer)/60.0, " minutes"
