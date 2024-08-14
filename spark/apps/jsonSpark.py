from pyspark.sql import SparkSession
from pymongo import MongoClient

# Création de la session Spark
spark = SparkSession.builder \
    .appName("JSON to HDFS and MongoDB Integration") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Lire les données depuis un fichier JSON
json_path = "/opt/spark-apps/data.json"
df_spark = spark.read.option("multiLine", true).json(json_path)

# Afficher les données lues depuis le fichier JSON
df_spark.show(truncate=False)

# Sauvegarder les résultats dans HDFS au format Parquet
df_spark.write \
    .format("parquet") \
    .mode("overwrite") \
    .save("hdfs://namenode:8020/filtered_data")

# Lire les données depuis HDFS
hdfsDF = spark.read \
    .format("parquet") \
    .load("hdfs://namenode:8020/filtered_data")

# Afficher les données lues depuis HDFS
hdfsDF.show(truncate=False)

# Convertir le DataFrame Spark en liste de dictionnaires pour MongoDB
data_to_insert = hdfsDF.toPandas().to_dict(orient='records')

# Connexion à MongoDB avec pymongo
client = MongoClient("mongodb://mongo:27017/")
db = client['testdb']
collection = db['testcollection2']

# Insérer les données dans MongoDB par lots
batch_size = 1000
for i in range(0, len(data_to_insert), batch_size):
    batch = data_to_insert[i:i + batch_size]
    collection.insert_many(batch)

# Fermer la connexion à MongoDB
client.close()

# Arrêter la session Spark
spark.stop()
