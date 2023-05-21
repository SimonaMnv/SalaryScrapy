#!/usr/bin/env bash
set -e

source scripts/vars.sh

scripts/setup_python.sh

pip install --upgrade pip

pip install wheel

pip install -r ./requirements.txt
