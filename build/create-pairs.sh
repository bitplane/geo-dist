#!/bin/bash

source .venv/bin/activate

set -e

echo "Creating data"

python -m geo_dist_prep.create_data
