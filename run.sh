#!/bin/bash

# Get latest geonames dump
geoNamesURL=https://github.com/geometalab/OSMNames/releases/download/v2.0/planet-latest_geonames.tsv.gz
geoNamesFile=.cache/geonames.tsv.gz

wget --continue --timestamping "$geoNamesURL" -O "$geoNamesFile"

zcat "$geoNamesFile" | ./filter_geonames.py > .cache/filtered.tsv
