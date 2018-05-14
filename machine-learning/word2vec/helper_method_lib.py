#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""Helper Method
"""


import re
import nltk
from pyspark.sql import Row
from pyspark.sql import functions as func
from pyspark.sql.functions import udf
from pyspark.sql.types import BooleanType

def helper_method_process_data(total_data, spark_context, sql_context):
    """ Process the raw input data

    This function parallelize and filter raw input data 
    to be ready for model building.

    Keyword arguments:
    total_data -- raw input data
    spark_context -- Spark context created in caller module
    sql_context -- SQL/HIVE Context created in caller module

    """
    def table_creator(row):
        '''
        This method will give minimal structure to data asper requirement. 
        '''
        temp_file_name = str(row['ci_job']['artifacts'].get('name',''))
        return(Row(
                original_url = str(row['ci_job']['artifacts'].get('original_url','')),
                result = str(row['ci_job'].get('result','')),
                message = row.get('message',''),
                file_name = 'XML' if temp_file_name.endswith('.xml') else temp_file_name,  
                )
            )

    def datetime_substitutor(a): 
        return re.sub('\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}','', a)

    def space_remover(a):
        return re.sub('\s+',' ',a)

    def caller_method(a):
        return space_remover(datetime_substitutor(a))
    

    print "===============One data point=============:"
    print "inside  helper_method_process_data KEYS:", total_data[0].keys()
    
    print "After filtering out the data without _source, length of data:", len(total_data)
    
    total_df = spark_context.parallelize(total_data).map(table_creator)
    
    total_df = total_df.filter(lambda a:a.original_url.endswith('xunit.xml') == False)

    total_df = sql_context.createDataFrame(data = total_df, samplingRatio = 0.3)
    
    udf_caller_method = udf(caller_method)

    #msg_df_failed = total_df.rdd.filter(lambda a:a.result != 'SUCCESS').toDF(sampleRatio=0.3).select('message','original_url')
    msg_df_failed = total_df.select('message','original_url')

    msg_df_failed = msg_df_failed.withColumn("cleaned_message", udf_caller_method(msg_df_failed.message))

    msg_df_failed.first()

    #regex = re.compile('[%s]' % re.escape(string.punctuation))

    color_code_words = ['[1;32m', '[0m']

    stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards']
    stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
    stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
    stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
    stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
    stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
    stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
    stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
    stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
    stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
    stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']
    stopwords += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']
    stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
    stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
    stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
    stopwords += ['false','few', 'fifteen', 'fifty', 'file', 'fill', 'find', 'fire', 'first']
    stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
    stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
    stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
    stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
    stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
    stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
    stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
    stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'line', 'ltd', 'made']
    stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
    stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
    stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
    stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
    stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
    stopwords += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']
    stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
    stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
    stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
    stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
    stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
    stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
    stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
    stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
    stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
    stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
    stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
    stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
    stopwords += ['together', 'too', 'top', 'toward', 'towards', 'true', 'twelve']
    stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
    stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
    stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
    stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
    stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
    stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
    stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']
    stopwords += ['yours', 'yourself', 'yourselves']
    stopwords += color_code_words
    stopwords = set(stopwords)
    
    broadcast_var = spark_context.broadcast(stopwords)

    total_df.unpersist()
    del total_df
    
    ## Notes: Map Reduce was replaced by Aggregation of Spark Framework. 
    temp_df = msg_df_failed.filter(udf(lambda x: x.strip() != '', BooleanType())(msg_df_failed.cleaned_message)).groupby('original_url').agg(func.concat_ws(" ", func.collect_list(msg_df_failed.cleaned_message))).withColumnRenamed("original_url","artifact_url").withColumnRenamed("concat_ws( , collect_list(cleaned_message))","concat_msg")
    
    print "=================== NLTK version Print====================="
    print nltk.__version__

    
    def word_tokenize(x):
        return nltk.word_tokenize(x)
    
    
    df = (temp_df
          .rdd
          .map(lambda x : (x.artifact_url, word_tokenize(x.concat_msg))).toDF()
          .withColumnRenamed("_1","artifact_url")).withColumnRenamed("_2","features")

    temp_df.unpersist()
    msg_df_failed.unpersist()

    del temp_df 
    del msg_df_failed
    
    df = df.rdd.map(lambda a:Row(artifact_url= a.artifact_url, features= filter(lambda y:len(y)>3, [x.lower() for x in a.features])))        .map(lambda a:Row(artifact_url= a.artifact_url, features= filter(lambda x:(x not in broadcast_var.value),a.features))).toDF()

    return df

