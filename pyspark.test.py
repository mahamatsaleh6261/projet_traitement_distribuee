from pyspark.sql import SparkSession
from pymongo import MongoClient
import pandas as pd

# Création de la session Spark
spark = SparkSession.builder \
    .appName("MongoDB and Hadoop Integration Job") \
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

# Convertir le DataFrame pandas en DataFrame Spark
df_spark = spark.createDataFrame(df_pandas)

# Afficher les données lues depuis MongoDB
df_spark.show(truncate=False)

# Exemple de filtre: sélectionner les restaurants avec un score supérieur à 15 dans les notes
filteredDF = df_spark \
    .withColumn("grades", explode(col("grades"))) \
    .filter(col("grades.score") > 15) \
    .select(
        col("name"),
        col("address.street"),
        col("address.zipcode"),
        col("grades.grade"),
        col("grades.score")
    )

# Afficher les données filtrées
filteredDF.show(truncate=False)

# Sauvegarder les résultats filtrés dans HDFS au format Parquet
filteredDF.write \
    .format("parquet") \
    .mode("overwrite") \
    .save("hdfs://namenode:8020/filtered_data")

# Lire les données depuis HDFS
hdfsDF = spark.read \
    .format("parquet") \
    .load("hdfs://namenode:8020/filtered_data")

# Afficher les données lues depuis HDFS
hdfsDF.show(truncate=False)

# Convertir le DataFrame Spark en Pandas DataFrame pour utiliser pymongo
hdfs_pd_df = hdfsDF.toPandas()

# Convertir le DataFrame pandas en dictionnaires et insérer les données dans MongoDB
data_to_insert = hdfs_pd_df.to_dict(orient='records')
collection.insert_many(data_to_insert)

# Fermer la connexion à MongoDB
client.close()

# Arrêter la session Spark
spark.stop()
