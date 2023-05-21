#!/usr/bin/env bash
set -e

scripts/setup_python.sh

pip install --upgrade pip

pip install wheel

pip install -r ./requirements.txt
