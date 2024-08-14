#!/bin/bash
echo "Importing data into MongoDB..."

mongoimport --db testdb --collection testcollection --file /data/data.json --jsonArray

echo "Data import completed."
