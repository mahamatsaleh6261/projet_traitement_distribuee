import org.apache.spark.sql.{SparkSession, DataFrame}
import org.apache.spark.sql.functions._

object MongoDBJob {
  def main(args: Array[String]): Unit = {
    // Créer la session Spark avec la configuration de MongoDB
    val spark = SparkSession.builder()
      .appName("MongoDB and Hadoop Integration Job")
      .config("spark.master", "spark://spark-master:7077")
      .config("spark.mongodb.input.uri", "mongodb://mongo:27017/testdb.testcollection")
      .config("spark.mongodb.output.uri", "mongodb://mongo:27017/testdb.testcollection")
      .getOrCreate()

    // Lire les données depuis MongoDB
    val mongoDF: DataFrame = spark.read
      .format("com.mongodb.spark.sql")
      .option("uri", "mongodb://mongo:27017/testdb.testcollection")
      .load()

    // Afficher les données lues depuis MongoDB
    mongoDF.show(false)

    // Exemple de filtre: sélectionner les restaurants avec un score supérieur à 15 dans les notes
    val filteredDF = mongoDF
      .withColumn("grades", explode(col("grades"))) // Déplie la colonne grades
      .filter(col("grades.score") > 15)
      .select(
        col("name"),
        col("address.street"),
        col("address.zipcode"),
        col("grades.grade"),
        col("grades.score")
      )

    // Afficher les données filtrées
    filteredDF.show(false)

    // Sauvegarder les résultats filtrés dans HDFS au format Parquet
    filteredDF.write
      .format("parquet")
      .mode("overwrite")
      .save("hdfs://namenode:8020/filtered_data")

    // Lire les données depuis HDFS
    val hdfsDF: DataFrame = spark.read
      .format("parquet")
      .load("hdfs://namenode:8020/filtered_data")

    // Afficher les données lues depuis HDFS
    hdfsDF.show(false)

    // Sauvegarder les résultats dans MongoDB
    hdfsDF.write
      .format("com.mongodb.spark.sql")
      .option("uri", "mongodb://mongo:27017/testdb.testcollection")
      .mode("append")
      .save()

    // Arrêter la session Spark
    spark.stop()
  }
}
