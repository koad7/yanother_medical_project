from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, FloatType

spark = SparkSession.builder \
    .appName("HealthDataProcessor") \
    .getOrCreate()

# Define schema for each type of data
heart_rate_schema = StructType([StructField("heart_rate", FloatType(), True)])
body_temp_schema = StructType([StructField("body_temperature", FloatType(), True)])
bp_schema = StructType([StructField("blood_pressure", StringType(), True)])
oxygen_schema = StructType([StructField("O2_saturation", FloatType(), True)])

# Function to create DataFrame for each topic
def create_df(topic, schema):
    return spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", topic) \
        .load() \
        .selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")

# Create DataFrames for each topic
heart_rate_df = create_df('heart_rate', heart_rate_schema)
body_temp_df = create_df('body_temperature', body_temp_schema)
bp_df = create_df('blood_pressure', bp_schema)
oxygen_df = create_df('peripheral_oxygen_saturation', oxygen_schema)

# Write data to console (or other sinks like HDFS, S3, etc.)
query1 = heart_rate_df.writeStream.outputMode("append").format("console").start()
query2 = body_temp_df.writeStream.outputMode("append").format("console").start()
query3 = bp_df.writeStream.outputMode("append").format("console").start()
query4 = oxygen_df.writeStream.outputMode("append").format("console").start()

query1.awaitTermination()
query2.awaitTermination()
query3.awaitTermination()
query4.awaitTermination()
