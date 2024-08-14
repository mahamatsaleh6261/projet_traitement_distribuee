from pyspark.sql import SparkSession

# Créer une session Spark
spark = SparkSession.builder \
    .appName("Read Parquet File") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Lire les fichiers Parquet depuis HDFS
df = spark.read \
    .parquet("hdfs://namenode:8020/filtered_data")

# Afficher le contenu du DataFrame
df.show(truncate=False)

# Arrêter la session Spark
spark.stop()
