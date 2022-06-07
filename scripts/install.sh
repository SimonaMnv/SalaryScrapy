#!/usr/bin/env bash
set -e

chmod 755 scripts/setup_python.sh
scripts/setup_python.sh

pip install --upgrade pip

pip install wheel

pip install -r ./requirements.txt