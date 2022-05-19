"""
These tests exist just to confirm that new definitions are working as
expected.
"""

import json
from pathlib import Path

import pytest

from xpring import serialization

test_dir = Path(__file__).parent
TRANSACTION_EXAMPLES = json.load((test_dir / 'transactions.json').open())

@pytest.mark.parametrize('transaction', TRANSACTION_EXAMPLES)
def test_serialize_transaction(transaction):
    blob = serialization.serialize_transaction(transaction)
    assert blob.hex()
