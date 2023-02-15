from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract

spark = SparkSession.builder.appName("PySpark Nasa logs").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
sc = spark.sparkContext


logs = spark.read.text("file:///C:/Users/didac.blanco/Desktop/sampledata/nasa logs/logs")
regex = "^([^ ]+) - - \\[(\\d{2}/\\w{3}/\\d{4}:\\d{2}:\\d{2}:\\d{2}).*?\\] \"(.*?) (.*?)(HTTP/.*?) *?\" (.+?) (.*+)"
df = logs.select(
    regexp_extract("value", regex, 1).alias("host"),
    regexp_extract("value", regex, 2).alias("date"),
    regexp_extract("value", regex, 3).alias("method"),
    regexp_extract("value", regex, 4).alias("resource"),
    regexp_extract("value", regex, 5).alias("protocol"),
    regexp_extract("value", regex, 6).alias("status"),
    regexp_extract("value", regex, 7).alias("size").cast("int")
  )
df.show(5, False)
df.printSchema()