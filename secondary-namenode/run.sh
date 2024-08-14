#!/bin/bash

# Check if checkpoint dir exists
checkpointdir=`echo $HDFS_CONF_dfs_checkpoint_dir | perl -pe 's#file://##'`
if [ ! -d $checkpointdir ]; then
  echo "Checkpoint directory not found: $checkpointdir"
  exit 2
fi

# Start secondary namenode service
$HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR secondarynamenode
