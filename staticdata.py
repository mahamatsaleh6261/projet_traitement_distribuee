from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pymongo import MongoClient

# Création de la session Spark sans configuration MongoDB URI
spark = SparkSession.builder \
    .appName("Static DataFrame to HDFS and MongoDB") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Création d'un DataFrame Spark statique
data = [
    ("Alice", "New York", 30),
    ("Bob", "San Francisco", 25),
    ("Charlie", "Boston", 35),
    ("David", "New York", 40),
    ("Eve", "San Francisco", 22)
]
columns = ["name", "city", "age"]
df_spark = spark.createDataFrame(data, columns)

# Afficher le DataFrame initial
print("DataFrame initial:")
df_spark.show(truncate=False)

# Filtrer les données (exemple : sélectionner les personnes âgées de plus de 30 ans)
filteredDF = df_spark.filter(col("age") > 30)

# Afficher les données filtrées
print("DataFrame filtré:")
filteredDF.show(truncate=False)

# Sauvegarder les résultats filtrés dans HDFS au format Parquet
hdfs_path = "hdfs://namenode:8020/filtered_data"
filteredDF.write \
    .format("parquet") \
    .mode("overwrite") \
    .save(hdfs_path)

# Lire les données depuis HDFS
hdfsDF = spark.read \
    .format("parquet") \
    .load(hdfs_path)

# Afficher les données lues depuis HDFS
print("Données lues depuis HDFS:")
hdfsDF.show(truncate=False)

# Convertir le DataFrame Spark en liste de dictionnaires pour MongoDB
data_to_insert = hdfsDF.toPandas().to_dict(orient='records')

# Connexion à MongoDB avec pymongo
client = MongoClient("mongodb://mongo:27017/")
db = client['testdb']
collection = db['testcollection2']

# Insérer les données dans MongoDB
collection.insert_many(data_to_insert)

# Vérifier les données dans MongoDB
print("Données insérées dans MongoDB:")
for doc in collection.find():
    print(doc)

# Fermer la connexion à MongoDB
client.close()

# Arrêter la session Spark
spark.stop()
