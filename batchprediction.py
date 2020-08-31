import os
import sys
import mlflow
import mlflow.pyfunc
os.environ['PYSPARK_PYTHON']= "/Users/ravishankarnair/anaconda3/envs/py36/bin/python3"
os.environ['PYSPARK_DRIVER_PYTHON']= "/Users/ravishankarnair/anaconda3/envs/py36/bin/python3"
os.environ['PYLIB'] = os.environ['SPARK_HOME'] + "/python/lib"
sys.path.insert(0,os.environ['PYLIB'] + 'py4j-0.10.9-src.zip')
sys.path.insert(0,os.environ['PYLIB'] + 'pyspark.zip')
from pyspark.sql import SparkSession
from pyspark.sql.types import ArrayType, StringType
from pyspark.sql.functions import udf, struct


spark = SparkSession.builder \
        .master("spark://ravion.local:7077") \
        .appName("OneClickBatchExecution") \
        .config("spark.executor.memory", "5G") \
        .config("spark.driver.memory", "5G") \
        .config("spark.debug.maxToStringFields", "10000") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .getOrCreate()

wine_x =  spark.read.format("csv") \
  .option("inferSchema", "true" )\
  .option("header", "true") \
  .option("sep", ",")  \
  .load("file:///Users/ravishankarnair/sparkmagic/wine.data")


pyfunc_udf = mlflow.pyfunc.spark_udf(spark, model_uri="s3://sample/19/1c47cf5cd059441baf78338a5dfce4fe/artifacts/wine_pyfunc" , result_type = ArrayType(StringType()))

dataframe = wine_x.drop("Class label")
df = dataframe.withColumn("prediction", pyfunc_udf(struct('Alcohol', 'Malic acid', 'Ash', 'Alcalinity of ash', 'Magnesium', 'Total phenols', 'Flavanoids', 'Nonflavanoid phenols', 'Proanthocyanins', 'Color intensity', 'Hue', 'OD280/OD315 of diluted wines', 'Proline')))
df.show(10)
