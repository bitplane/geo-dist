#!/bin/bash

# Get latest geonames dump
geoNamesURL=https://github.com/geometalab/OSMNames/releases/download/v2.0/planet-latest_geonames.tsv.gz
geoNamesFile=.cache/geonames.tsv.gz


echo "Downloading geonames file to $geoNamesFile"

wget --continue --timestamping "$geoNamesURL" -O "$geoNamesFile"


echo "Filtering geonames"

zcat "$geoNamesFile" | ./filter_geonames.py > .cache/filtered.tsv

./node_tree.py .cache/filtered.tsv > .cache/nodes.json
