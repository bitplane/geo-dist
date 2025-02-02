#!/usr/bin/env bash
# build/train.sh - run model training

source .venv/bin/activate

set -e

echo "Starting model training..."
python3 -m geo_dist_prep.model.train

# Create a cache marker to indicate training is done.
touch .cache/train.done
