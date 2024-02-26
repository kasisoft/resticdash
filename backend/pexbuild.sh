#!/bin/bash
export DIRNAME=$(readlink -f  $(dirname $0))
export CURRENTDIR=$(pwd)
cd "${DIRNAME}"
if [ ! -d "${DIRNAME}/venv" ]; then
    python3 -m pip install --user virtualenv
    virtualenv venv
fi
source "./venv/bin/activate"
pip3 install -r requirements.txt
pex -D src/main -r requirements.txt -e ${1} -o app.pex
cd "${CURRENTDIR}"
