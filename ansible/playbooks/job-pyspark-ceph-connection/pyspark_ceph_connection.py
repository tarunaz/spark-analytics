#Import the PySpark library
import pyspark 
from pyspark import SparkContext

#Set the Spark cluster connection
sc = SparkContext() 

#Set the Hadoop configurations to access Ceph S3
sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", 'IREC3HIIFZ2WMB9UA9U8') 
sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", 'gETnAsfiC4v5coC91n7ADHjdeAxI53bpC52f8ivA') 
sc._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", 'false') 
sc._jsc.hadoopConfiguration().set("fs.s3a.endpoint", 'http://storage-016.infra.prod.upshift.eng.rdu2.redhat.com:8080') 

#Get the SQL context
sqlContext = pyspark.SQLContext(sc)

#Read the SQL parquet data
parquetFile = sqlContext.read.parquet("s3a://DH-DEV-INSIGHTS/2018-02-28/insights_parsers_cpuinfo_cpuinfo/part-00123-085eabf2-830d-4508-bbde-de23d651794c-c000.snappy.parquet") 

#Display the output
parquetFile.show()  


print('Done reading') 
