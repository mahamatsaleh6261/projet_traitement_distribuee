FROM openjdk:11-jdk

USER root

# --------------------------------------------------------
# Install Python
# --------------------------------------------------------
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------
# HADOOP
# --------------------------------------------------------
ENV HADOOP_VERSION=3.3.1
ENV HADOOP_URL=https://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz
ENV HADOOP_PREFIX=/opt/hadoop-$HADOOP_VERSION
ENV HADOOP_CONF_DIR=/etc/hadoop
ENV MULTIHOMED_NETWORK=1
ENV USER=root
ENV HADOOP_HOME=/opt/hadoop-$HADOOP_VERSION

# 
ENV PATH=$HADOOP_PREFIX/bin:$HADOOP_HOME/bin:$PATH

RUN set -x \
    && curl -fSL "$HADOOP_URL" -o /tmp/hadoop.tar.gz \
    && tar -xvf /tmp/hadoop.tar.gz -C /opt/ \
    && rm /tmp/hadoop.tar.gz*

RUN ln -s /opt/hadoop-$HADOOP_VERSION/etc/hadoop /etc/hadoop
RUN mkdir /opt/hadoop-$HADOOP_VERSION/logs
RUN mkdir /hadoop-data

# --------------------------------------------------------
# MongoDB-Hadoop Connector
# --------------------------------------------------------
ENV HADOOP_MONGODB_CONNECTOR_VERSION=2.0.2
ENV HADOOP_MONGODB_CONNECTOR_URL=https://repo1.maven.org/maven2/org/mongodb/mongo-hadoop/mongo-hadoop-spark/$HADOOP_MONGODB_CONNECTOR_VERSION/mongo-hadoop-spark-$HADOOP_MONGODB_CONNECTOR_VERSION.jar

RUN mkdir -p /opt/hadoop-$HADOOP_VERSION/share/hadoop/common/lib \
    && set -x \
    && curl -fSL "$HADOOP_MONGODB_CONNECTOR_URL" -o /opt/hadoop-$HADOOP_VERSION/share/hadoop/common/lib/mongo-hadoop-spark-$HADOOP_MONGODB_CONNECTOR_VERSION.jar

# Set the HADOOP_CLASSPATH 
ENV HADOOP_CLASSPATH=$HADOOP_HOME/share/hadoop/common/lib/mongo-hadoop-spark-$HADOOP_MONGODB_CONNECTOR_VERSION.jar


# USER root

COPY conf/core-site.xml $HADOOP_CONF_DIR/core-site.xml
COPY conf/hdfs-site.xml $HADOOP_CONF_DIR/hdfs-site.xml
COPY conf/mapred-site.xml $HADOOP_CONF_DIR/mapred-site.xml
COPY conf/yarn-site.xml $HADOOP_CONF_DIR/yarn-site.xml

# --------------------------------------------------------
# SPARK
# --------------------------------------------------------
ENV SPARK_VERSION=spark-3.3.1-bin-hadoop3
ENV SPARK_URL=https://archive.apache.org/dist/spark/spark-3.3.1/$SPARK_VERSION.tgz
ENV SPARK_HOME=/opt/$SPARK_VERSION

# 
ENV PATH=$SPARK_HOME/bin:$PATH
ENV PYSPARK_PYTHON=python3
ENV PYTHONHASHSEED=1

RUN set -x \
    && curl -fSL "$SPARK_URL" -o /tmp/spark.tar.gz \
    && tar -xvzf /tmp/spark.tar.gz -C /opt/ \
    && rm /tmp/spark.tar.gz*

ADD conf/core-site.xml $SPARK_HOME/conf
ADD conf/yarn-site.xml $SPARK_HOME/conf

# --------------------------------------------------------
# Installation de Apache Pig
# --------------------------------------------------------
ENV PIG_VERSION=0.17.0
ENV PIG_URL=https://archive.apache.org/dist/pig/pig-$PIG_VERSION/pig-$PIG_VERSION.tar.gz
ENV PIG_HOME=/opt/pig-$PIG_VERSION
ENV PATH=$PIG_HOME/bin:$PATH

RUN set -x \
    && curl -fSL "$PIG_URL" -o /tmp/pig.tar.gz \
    && tar -xvzf /tmp/pig.tar.gz -C /opt/ \
    && rm /tmp/pig.tar.gz* \
    && ln -s /opt/pig-$PIG_VERSION /opt/pig

# 
RUN pig -version

# default command
CMD ["bash"]