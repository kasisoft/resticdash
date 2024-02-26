#!/bin/bash
export DIRNAME=$(readlink -f  $(dirname $0))
source "${DIRNAME}/venv/bin/activate"
pex "${DIRNAME}" -D src/main -r "${DIRNAME}/requirements.txt" -e ${1} -o "${DIRNAME}/app.pex"
