from pyspark.sql import SparkSession
import pytest

@pytest.fixture(scope="module")
def spark():
    spark = SparkSession.builder \
        .master("local[2]") \
        .appName("test") \
        .getOrCreate()
    yield spark
    spark.stop()

def test_schema(spark):
    from pyspark.sql.types import StructType, StructField, StringType, FloatType
    from consumer.consumer import create_df

    schema = StructType([
        StructField("heart_rate", FloatType(), True)
    ])
    
    data = [("85",), ("90",)]
    df = spark.createDataFrame(data, ["heart_rate"])

    df_schema = create_df('test_topic', schema).schema
    assert df_schema == schema
