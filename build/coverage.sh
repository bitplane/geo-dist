#!/usr/bin/env bash

source .venv/bin/activate

pytest --cov=geo-dist-prep/src --cov-report=html .
