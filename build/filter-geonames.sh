#!/bin/bash

source .venv/bin/activate

set -e

echo "Filtering geonames"

zcat .cache/geonames.tsv.gz | python -m geo_dist_prep.filter_geonames > .cache/filtered-geonames.tsv
