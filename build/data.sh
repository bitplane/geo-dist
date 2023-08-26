#!/bin/bash

source .venv/bin/activate

set -e

echo "Running step: $1"

python -m "geo_dist_prep.data.$1"
