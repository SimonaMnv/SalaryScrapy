#!/usr/bin/env bash

set -e

WANTED_VERSION=`cat .python-version | cut -f 1 -d '/'`
echo "Wanted python version: ${WANTED_VERSION}"
VENV_NAME=`cat .python-version | cut -f 3 -d '/'`
echo "Virtual environment name: ${VENV_NAME}"

CURDIR=${PWD##*/}

pyenv install -s ${WANTED_VERSION}

echo "Setting up virtual environment..."

pyenv virtualenv ${WANTED_VERSION} ${VENV_NAME} || true

#allow pyenv to activate the virtual env
cd ../${CURDIR}

echo "Listing virtual environments..."

pyenv virtualenvs

WHICH_PY=`which python`
echo "Python found at: ${WHICH_PY}"

if [[ "${WHICH_PY}" == "/usr/bin/python" ]]; then
  echo "System python should not be used, as dependencies can be problematic"
  exit 1
fi

PY_VERSION=`python --version 2>&1| cut -d " " -f 2`
echo "Python version found: ${PY_VERSION}"

if [[ "${PY_VERSION}" != "${WANTED_VERSION}" ]]; then
  echo "Python version mismatch (${PY_VERSION} != ${WANTED_VERSION}) , please check that you are running the version of python specified in the .python-version file"
  exit 2
fi