docker tag hadoop-base:3.3.1 kor7mid/hadoop-spark-base:1.0.0
docker push kor7mid/hadoop-spark-base:1.0.0

//===================================================
docker tag spark-base:3.3.1 kor7mid/spark-base:1.0.0
docker push kor7mid/spark-base:1.0.0

docker build -t kor7mid/hadoop-spark-base:1.0.3 .
docker build -t kor7mid/spark-base:1.0.3 .

//===================================================
sudo chmod +x file.sh
//=====================================================
pig installer
//============= mongo
mongo-init/
├── data.json
├── init.js
└── init.sh

https://data.europa.eu/data/datasets?locale=en //data mongo
docker exec -it 4e4c0a5a4643 mongosh
use testdb
show collections
db.testcollection.find().pretty()
//========================================

hadoop connector mongo testing after connection
//=========recap
docker exec -it 19c308122c6c /bin/bash <hadoop_container_name>
hdfs dfsadmin -report // verifier lestatus des names nodes des des datanodes,
hdfs dfs -ls / // commade pour lister les fichiers

docker exec -it 651d35d11c79 /bin/bash <spark_container_name> //spark testing
spark-shell --master spark://<spark_master_host>:<spark_master_port>
spark-shell --master spark://spark-master:7077
docker cp /home/midekor/Documents/Coding/examen-apeke-TD-BigData/hadoop-docker-final/MongoDBJob.scala 651d35d11c79:/opt/spark-apps/MongoDBJob.scala //<spark_container_id>

:load /opt/spark-apps/MongoDBJob.scala

MongoDBJob.main(Array.empty[String])
//===========aproche 2 utilisation de pymongo dans pyspark,

pip install pymongo pyspark pandas && pip install pyarrow --upgrade
docker cp /home/midekor/Documents/Coding/examen-apeke-TD-BigData/hadoop-docker-final/pyspark.test.py 651d35d11c79:/opt/spark-apps/pyspark.test.py
spark-submit /opt/spark-apps/pyspark.test.py

docker cp /home/midekor/Documents/Coding/examen-apeke-TD-BigData/hadoop-docker-final/data.json 651d35d11c79:/opt/spark-apps/data.json

docker cp /home/midekor/Documents/Coding/examen-apeke-TD-BigData/hadoop-docker-final/staticdata.py 651d35d11c79:/opt/spark-apps/staticdata.py
spark-submit /opt/spark-apps/staticdata.py

docker exec -it fef0e627c76d /bin/bash <namenode_container_id>
hdfs dfs -ls /filtered_data
hdfs dfs -cat /filtered_data/part-00000

//=======job
Charger les données depuis un fichier JSON.
Convertir ces données en DataFrame Spark.
Effectuer les opérations nécessaires.
Enregistrer les résultats dans HDFS.
Lire les données depuis HDFS.
Enregistrer les résultats dans MongoDB.
//======================================
