import hashlib
import typing as t

import pytest

from xpring import hashes

SECP256K1_SIGNATURE_EXAMPLES = (
    ('signing_key_hex', 'message_digest_hex', 'signature_hex'),
    [
        # https://github.com/btccom/secp256k1-go/blob/f7178bcde5780809c6f819d62c3e7a37c635e749/secp256k1/sign_vectors.yaml#L3-L5
        pytest.param(
            '31a84594060e103f5a63eb742bd46cf5f5900d8406e2726dedfc61c7cf43ebad',
            '9e5755ec2f328cc8635a55415d0e9a09c2b6f2c9b0343c945fbbfe08247a4cbe',
            '30440220132382ca59240c2e14ee7ff61d90fc63276325f4cbe8169fc53ade4a407c2fc802204d86fbe3bde6975dd5a91fdc95ad6544dcdf0dab206f02224ce7e2b151bd82ab',
            id='31a845',
        ),
        # https://github.com/btccom/secp256k1-go/blob/f7178bcde5780809c6f819d62c3e7a37c635e749/secp256k1/sign_vectors.yaml#L16-L18
        pytest.param(
            '39dfc615f2b718397f6903b0c46c47c5687e97d3d2a5e1f2b200f459f7b1219b',
            'dfeb2092955572ce0695aa038f58df5499949e18f58785553c3e83343cd5eb93',
            '30440220692c01edf8aeab271df3ed4e8d57a170f014f8f9d65031aac28b5e1840acfb5602205075f9d1fdbf5079ee052e5f3572d518b3594ef49582899ec44d065f71a55192',
            id='39dfc6',
        ),
        # https://github.com/ripple/ripple-keypairs/blob/master/test/fixtures/api.json#L2-L11
        (
            'd78b9735c3f26501c7337b8a5727fd53a6efdbc6aa55984f098488561f985e23',
            # sha512half(b'test message')
            '950b2a7effa78f51a63515ec45e03ecebe50ef2f1c41e69629b50778f11bc080',
            '30440220583a91c95e54e6a651c47bec22744e0b101e2c4060e7b08f6341657dad9bc3ee02207d1489c7395db0188d3a56a977ecba54b36fa9371b40319655b1b4429e33ef2d',
        ),
    ]
)


class Sha512Half:
    digest_size = 32
    block_size = hashlib.sha512().block_size
    name = 'sha512half'

    def __init__(self, data: bytes = b'') -> None:
        self.data = bytes(data)

    def update(self, data: bytes) -> None:
        self.data += bytes(data)

    def digest(self) -> bytes:
        return hashes.sha512half(self.data)

    def hexdigest(self) -> str:
        return self.digest().hex()

    def copy(self) -> 'Sha512Half':
        return self.__class__(self.data)
