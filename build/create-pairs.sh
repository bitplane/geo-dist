#!/bin/bash

source .venv/bin/activate

set -e

echo "Creating pairs"

python -m geo_dist_prep.create_pairs
