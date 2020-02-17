import pytest

import xpring.serialization as serialization

# yapf: disable
TRANSACTION_EXAMPLES = (
    ('transaction', 'blob_hex'), (
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
        # https://github.com/ripple/xrpl-dev-portal/tree/57dd03d9a1ff610c12c692ead93a6acb06cfe950/content/_code-samples/tx-serialization/test-cases
        (
            # tx1.json
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
                'hash': '73734B611DDA23D3F5F62E20A173B78AB8406AC5015094DA53F53D39B9EDB06C'
            },
            # tx1-binary.txt
            '120007220008000024001ABED82A2380BF2C2019001ABED764D55920AC9391400000000000000000000000000055534400000000000A20B3C85F482532A9578DBB3950B85CA06594D165400000037E11D60068400000000000000A732103EE83BB432547885C219634A1BC407A9DB0474145D69737D09CCDC63E1DEE7FE3744630440220143759437C04F7B61F012563AFE90D8DAFC46E86035E1D965A9CED282C97D4CE02204CFD241E86F17E011298FC1A39B63386C74306A5DE047E213B0F29EFA4571C2C8114DD76483FACDEE26E60D8A586BB58D09F27045C46',
        ),
        (
            # tx2.json
            {
                'TransactionType': 'EscrowFinish',
                'Flags': 2147483648,
                'Sequence': 1,
                'OfferSequence': 11,
                'Fee': '10101',
                'SigningPubKey': '0268D79CD579D077750740FA18A2370B7C2018B2714ECE70BA65C38D223E79BC9C',
                'TxnSignature': '3045022100F06FB54049D6D50142E5CF2E2AC21946AF305A13E2A2D4BA881B36484DD01A540220311557EC8BEF536D729605A4CB4D4DC51B1E37C06C93434DD5B7651E1E2E28BF',
                'Account': 'r3Y6vCE8XqfZmYBRngy22uFYkmz3y9eCRA',
                'Owner': 'r9NpyVfLfUG8hatuCCHKzosyDtKnBdsEN3',
                'Memos': [
                    {
                        'Memo': {
                            'MemoData': '04C4D46544659A2D58525043686174'
                        }
                    }
                ]
            },
            # tx2-binary.txt
            '1200022280000000240000000120190000000B68400000000000277573210268D79CD579D077750740FA18A2370B7C2018B2714ECE70BA65C38D223E79BC9C74473045022100F06FB54049D6D50142E5CF2E2AC21946AF305A13E2A2D4BA881B36484DD01A540220311557EC8BEF536D729605A4CB4D4DC51B1E37C06C93434DD5B7651E1E2E28BF811452C7F01AD13B3CA9C1D133FA8F3482D2EF08FA7D82145A380FBD236B6A1CD14B939AD21101E5B6B6FFA2F9EA7D0F04C4D46544659A2D58525043686174E1F1',
        ),
        (
            # tx3.json
            {
              'Account': 'rweYz56rfmQ98cAdRaeTxQS9wVMGnrdsFp',
              'Amount': '10000000',
              'Destination': 'rweYz56rfmQ98cAdRaeTxQS9wVMGnrdsFp',
              'Fee': '12',
              'Flags': 0,
              'LastLedgerSequence': 9902014,
              'Memos': [
                {
                  'Memo': {
                    'MemoData': '7274312E312E31',
                    'MemoType': '636C69656E74'
                  }
                }
              ],
              'Paths': [
                [
                  {
                    'account': 'rPDXxSZcuVL3ZWoyU82bcde3zwvmShkRyF',
                    'type': 1,
                    'type_hex': '0000000000000001'
                  },
                  {
                    'currency': 'XRP',
                    'type': 16,
                    'type_hex': '0000000000000010'
                  }
                ],
                [
                  {
                    'account': 'rf1BiGeXwwQoi8Z2ueFYTEXSwuJYfV2Jpn',
                    'type': 1,
                    'type_hex': '0000000000000001'
                  },
                  {
                    'account': 'rMwjYedjc7qqtKYVLiAccJSmCwih4LnE2q',
                    'type': 1,
                    'type_hex': '0000000000000001'
                  },
                  {
                    'currency': 'XRP',
                    'type': 16,
                    'type_hex': '0000000000000010'
                  }
                ]
              ],
              'SendMax': {
                'currency': 'USD',
                'issuer': 'rweYz56rfmQ98cAdRaeTxQS9wVMGnrdsFp',
                'value': '0.6275558355'
              },
              'Sequence': 842,
              'SigningPubKey': '0379F17CFA0FFD7518181594BE69FE9A10471D6DE1F4055C6D2746AFD6CF89889E',
              'TransactionType': 'Payment',
              'TxnSignature': '3045022100D55ED1953F860ADC1BC5CD993ABB927F48156ACA31C64737865F4F4FF6D015A80220630704D2BD09C8E99F26090C25F11B28F5D96A1350454402C2CED92B39FFDBAF',
              'hash': 'B521424226FC100A2A802FE20476A5F8426FD3F720176DC5CCCE0D75738CC208'
            },
            # tx3-binary.json
            '1200002200000000240000034A201B009717BE61400000000098968068400000000000000C69D4564B964A845AC0000000000000000000000000555344000000000069D33B18D53385F8A3185516C2EDA5DEDB8AC5C673210379F17CFA0FFD7518181594BE69FE9A10471D6DE1F4055C6D2746AFD6CF89889E74473045022100D55ED1953F860ADC1BC5CD993ABB927F48156ACA31C64737865F4F4FF6D015A80220630704D2BD09C8E99F26090C25F11B28F5D96A1350454402C2CED92B39FFDBAF811469D33B18D53385F8A3185516C2EDA5DEDB8AC5C6831469D33B18D53385F8A3185516C2EDA5DEDB8AC5C6F9EA7C06636C69656E747D077274312E312E31E1F1011201F3B1997562FD742B54D4EBDEA1D6AEA3D4906B8F100000000000000000000000000000000000000000FF014B4E9C06F24296074F7BC48F92A97916C6DC5EA901DD39C650A96EDA48334E70CC4A85B8B2E8502CD310000000000000000000000000000000000000000000',
        ),
    )
)
# yapf: enable


@pytest.mark.parametrize(*TRANSACTION_EXAMPLES)
def test_serialize_transaction(transaction, blob_hex):
    blob = serialization.serialize_object(transaction, mark=False)
    assert blob.hex().upper() == blob_hex


@pytest.mark.skip
@pytest.mark.parametrize(*TRANSACTION_EXAMPLES)
def test_deserialize_transaction(transaction, blob_hex):
    scanner = serialization.Scanner(bytes.fromhex(blob_hex))
    assert serialization.deserialize_object(scanner) == transaction


def test_codec_amount():
    amount = '12345'
    stream = serialization.serialize_amount(amount)
    scanner = serialization.Scanner(stream)
    assert serialization.deserialize_amount(scanner) == amount
