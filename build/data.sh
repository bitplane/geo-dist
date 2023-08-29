#!/bin/bash

source .venv/bin/activate

set -e

echo "Running step: $1"

python3 -m "geo_dist_prep.data.$1"

touch ".cache/$1.done"
