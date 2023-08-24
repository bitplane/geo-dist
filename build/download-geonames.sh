#!/bin/bash

# Get latest geonames dump
geoNamesURL="https://github.com/geometalab/OSMNames/releases/download/v2.0/planet-latest_geonames.tsv.gz"
outputFileName=".cache/geonames.tsv.gz"

filename=$(
    curl -L -I -s "$geoNamesURL" |
    grep -o -E 'filename=.*$' |
    sed -e 's/filename=//' -e 's/\r//'
)

echo "Downloading geonames file to $outputFileName"

pushd .cache && \
wget --continue "$geoNamesURL" &&
popd && \
    (
        ln -s "$filename" "$outputFileName"
        touch "$outputFileName".done
    )
