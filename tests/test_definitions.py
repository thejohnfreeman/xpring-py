"""
These tests exist just to confirm that new definitions are working as
expected.
"""

import pytest

from xpring import serialization

# yapf: disable
TRANSACTION_EXAMPLES = [
    (
        {
            'TransactionType': 'NFTokenMint',
            'Account': 'raFNCL4bUc8aSVNBc836y2ikMZoA56Bbvc',
            'Fee': '12',
            'TransferFee': 1,
            'TokenTaxon': 0,
            'Flags': 9,
            'URI': '4e4654206d696e742074657374',
        },
    )
]
# yapf: enable

@pytest.mark.parametrize(('transaction',), TRANSACTION_EXAMPLES)
def test_serialize_transaction(transaction):
    blob = serialization.serialize_transaction(transaction)
    assert blob.hex()
