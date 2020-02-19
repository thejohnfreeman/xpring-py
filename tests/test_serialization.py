import json
from pathlib import Path

import pytest

from xpring import hashes, serialization

# yapf: disable
TRANSACTION_EXAMPLES = [
    # https://xrpl.org/serialization.html#examples
    (
        {
            'Account': 'rMBzp8CgpE441cp5PVyA9rpVV7oT8hP3ys',
            'Expiration': 595640108,
            'Fee': '10',
            'Flags': 524288,
            'OfferSequence': 1752791,
            'Sequence': 1752792,
            'SigningPubKey': '03EE83BB432547885C219634A1BC407A9DB0474145D69737D09CCDC63E1DEE7FE3',
            'TakerGets': '15000000000',
            'TakerPays': {
                'currency': 'USD',
                'issuer': 'rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B',
                'value': '7072.8'
            },
            'TransactionType': 'OfferCreate',
            'TxnSignature': '30440220143759437C04F7B61F012563AFE90D8DAFC46E86035E1D965A9CED282C97D4CE02204CFD241E86F17E011298FC1A39B63386C74306A5DE047E213B0F29EFA4571C2C',
            'hash': '73734B611DDA23D3F5F62E20A173B78AB8406AC5015094DA53F53D39B9EDB06C',
        },
        '120007220008000024001ABED82A2380BF2C2019001ABED764D55920AC9391400000000000000000000000000055534400000000000A20B3C85F482532A9578DBB3950B85CA06594D165400000037E11D60068400000000000000A732103EE83BB432547885C219634A1BC407A9DB0474145D69737D09CCDC63E1DEE7FE3744630440220143759437C04F7B61F012563AFE90D8DAFC46E86035E1D965A9CED282C97D4CE02204CFD241E86F17E011298FC1A39B63386C74306A5DE047E213B0F29EFA4571C2C8114DD76483FACDEE26E60D8A586BB58D09F27045C46',
    ),
    # https://xrpl.org/sign.html
    # Input is `result.tx_json` of the response, minus the `hash` property.
    # Output is `result.tx_blob` of the response.
    (
        {
            'Account': 'rf1BiGeXwwQoi8Z2ueFYTEXSwuJYfV2Jpn',
            'Amount': {
                'currency': 'USD',
                'issuer': 'rf1BiGeXwwQoi8Z2ueFYTEXSwuJYfV2Jpn',
                'value': '1',
            },
            'Destination': 'ra5nK24KXen9AHvsdFTKHSANinZseWnPcX',
            'Fee': '10000',
            'Flags': 2147483648,
            'Sequence': 360,
            'SigningPubKey': '03AB40A0490F9B7ED8DF29D246BF2D6269820A0EE7742ACDD457BEA7C7D0931EDB',
            'TransactionType': 'Payment',
            'TxnSignature': '304402200E5C2DD81FDF0BE9AB2A8D797885ED49E804DBF28E806604D878756410CA98B102203349581946B0DDA06B36B35DBC20EDA27552C1F167BCF5C6ECFF49C6A46F8580',
            'hash': '4D5D90890F8D49519E4151938601EF3D0B30B16CD6A519D9C99102C9FA77F7E0',
        },
        '1200002280000000240000016861D4838D7EA4C6800000000000000000000000000055534400000000004B4E9C06F24296074F7BC48F92A97916C6DC5EA9684000000000002710732103AB40A0490F9B7ED8DF29D246BF2D6269820A0EE7742ACDD457BEA7C7D0931EDB7446304402200E5C2DD81FDF0BE9AB2A8D797885ED49E804DBF28E806604D878756410CA98B102203349581946B0DDA06B36B35DBC20EDA27552C1F167BCF5C6ECFF49C6A46F858081144B4E9C06F24296074F7BC48F92A97916C6DC5EA983143E9D4A2B8AA0780F682D136F7A56D6724EF53754',
    ),
]
# yapf: enable

# Go up two directories.
project_dir = Path(__file__).parents[1]
prefix = project_dir / 'submodules/xrpl-dev-portal/content/_code-samples/tx-serialization/test-cases'
for i in range(3):
    n = i + 1
    with (prefix / f'tx{n}.json').open() as file:
        transaction = json.load(file)
    blob_hex = (prefix / f'tx{n}-binary.txt').read_text().rstrip()
    TRANSACTION_EXAMPLES.append((transaction, blob_hex))

with (
    project_dir /
    'submodules/ripple-binary-codec/test/fixtures/codec-fixtures.json'
).open() as file:
    table = json.load(file)
for category, fixtures in table.items():
    # The ledgerData test uses undefined fields. Skip it.
    if category == 'ledgerData':
        continue
    for fixture in fixtures:
        TRANSACTION_EXAMPLES.append((fixture['json'], fixture['binary']))

# There are more tests here, but I would have to copy them by hand, and
# I think the ripple-binary-codec suite already gives us excellent coverage.
# https://github.com/ximinez/ripple-offline-tool/blob/master/src/test/KnownTestData.h

TRANSACTION_PARAMETERS = (('transaction', 'blob_hex'), TRANSACTION_EXAMPLES)


def without(dictionary, keys):
    return {k: v for k, v in dictionary.items() if k not in keys}


@pytest.mark.parametrize(*TRANSACTION_PARAMETERS)
def test_serialize_transaction(transaction, blob_hex):
    blob = serialization.serialize_transaction(transaction)
    assert blob.hex().upper() == blob_hex


@pytest.mark.parametrize(*TRANSACTION_PARAMETERS)
def test_deserialize_transaction(transaction, blob_hex):
    scanner = serialization.Scanner(bytes.fromhex(blob_hex))
    expected = without(transaction, ['hash'])
    assert serialization.deserialize_transaction(scanner) == expected


@pytest.mark.parametrize(*TRANSACTION_PARAMETERS)
def test_hash_transaction(transaction, blob_hex):
    if 'hash' not in transaction:
        return
    blob = serialization.PREFIX_TRANSACTION_ID + bytes.fromhex(blob_hex)
    digest = hashes.sha512half(blob)
    assert digest.hex().upper() == transaction['hash']


# yapf: disable
AMOUNT_EXAMPLES = (
    ('amount', 'blob_hex'),
    (
        ('12345', '4000000000003039'),
        (
            {
                'currency': 'USD',
                'issuer': 'rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B',
                'value': '7072.8',
            },
            'D55920AC9391400000000000000000000000000055534400000000000A20B3C85F482532A9578DBB3950B85CA06594D1',
        )
    )
)
# yapf: enable


@pytest.mark.parametrize(*AMOUNT_EXAMPLES)
def test_serialize_amount(amount, blob_hex):
    blob = serialization.serialize_amount(amount)
    assert blob.hex().upper() == blob_hex


@pytest.mark.parametrize(*AMOUNT_EXAMPLES)
def test_deserialize_amount(amount, blob_hex):
    scanner = serialization.Scanner(bytes.fromhex(blob_hex))
    assert serialization.deserialize_amount(scanner) == amount
