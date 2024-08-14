from pyspark.sql import SparkSession
from pymongo import MongoClient
import pandas as pd

# Création de la session Spark
spark = SparkSession.builder \
    .appName("MongoDB to Spark Integration") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Connexion à MongoDB avec pymongo
client = MongoClient("mongodb://mongo:27017/")
db = client['testdb']
collection = db['testcollection']

# Lire les données depuis MongoDB
data = list(collection.find())

# Convertir les données en DataFrame pandas
df_pandas = pd.DataFrame(data)

# Si nécessaire, convertir les types complexes
df_pandas['_id'] = df_pandas['_id'].astype(str)

# Convertir le DataFrame pandas en DataFrame Spark
df_spark = spark.createDataFrame(df_pandas)

# Afficher les données lues depuis MongoDB
df_spark.show(truncate=False)

# Fermer la connexion à MongoDB
client.close()

# Arrêter la session Spark
spark.stop()
