#!/usr/bin/env bash

set -o errexit
set -o nounset

PYTHON=${PYTHON:-python}

rm -rf venv
${PYTHON} -m venv venv
source venv/bin/activate
which ${PYTHON}
${PYTHON} -m pip install --upgrade pip
${PYTHON} -m pip install xpring fastecdsa

transactions=$(cat transactions.json)

${PYTHON} <<EOS
from xpring import serialization

transactions = ${transactions}
for transaction in transactions:
    serialization.serialize_transaction(transaction)
EOS
