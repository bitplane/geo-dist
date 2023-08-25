#!/bin/bash

source .venv/bin/activate

set -e

echo "Building tree"

python -m geo_dist_prep.build_tree
