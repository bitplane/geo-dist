#!/usr/bin/env bash

# activate venv
source .venv/bin/activate

set -e

# install our package
python3 -m pip install -e ./geo-dist-prep[dev]

touch .venv/.installed
