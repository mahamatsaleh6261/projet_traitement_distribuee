#!/bin/bash


# running image to container, -d to run it in daemon mode
docker-compose -f docker-compose-hadoop.yml down


# Run Spark Cluster
if [[ "$PWD" != "spark" ]]; then
  cd spark && ./stop-cluster.sh && cd ..
fi

echo "Current dir is $PWD"