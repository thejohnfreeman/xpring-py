import hashlib

from xpring import hashes

SECP256K1_SIGNATURE_EXAMPLES = (
    'private_key_bytes,message_hash_bytes,signature_bytes',
    tuple(
        map(
            lambda t: tuple(map(bytes.fromhex, t)),
            [
                # https://github.com/btccom/secp256k1-go/blob/f7178bcde5780809c6f819d62c3e7a37c635e749/secp256k1/sign_vectors.yaml#L3-L5
                (
                    '31a84594060e103f5a63eb742bd46cf5f5900d8406e2726dedfc61c7cf43ebad',
                    '9e5755ec2f328cc8635a55415d0e9a09c2b6f2c9b0343c945fbbfe08247a4cbe',
                    '30440220132382ca59240c2e14ee7ff61d90fc63276325f4cbe8169fc53ade4a407c2fc802204d86fbe3bde6975dd5a91fdc95ad6544dcdf0dab206f02224ce7e2b151bd82ab',
                ),
                # https://github.com/btccom/secp256k1-go/blob/master/secp256k1/sign_vectors.yaml#L8-L10
                (
                    '7177f0d04c79fa0b8c91fe90c1cf1d44772d1fba6e5eb9b281a22cd3aafb51fe',
                    '2d46a712699bae19a634563d74d04cc2da497b841456da270dccb75ac2f7c4e7',
                    '3045022100d80cf7abc9ab601373780cee3733d2cb5ff69ba1452ec2d2a058adf9645c13be0220011d1213b7d152f72fd8759b45276ba32d9c909602e5ec89550baf3aaa8ed950',
                ),
                # https://github.com/ripple/ripple-keypairs/blob/master/test/fixtures/api.json#L2-L11
                # (
                #     'd78b9735c3f26501c7337b8a5727fd53a6efdbc6aa55984f098488561f985e23',
                #     # sha512half(b'test message')
                #     '950b2a7effa78f51a63515ec45e03ecebe50ef2f1c41e69629b50778f11bc080',
                #     '30440220583a91c95e54e6a651c47bec22744e0b101e2c4060e7b08f6341657dad9bc3ee02207d1489c7395db0188d3a56a977ecba54b36fa9371b40319655b1b4429e33ef2d',
                # ),
            ]
        )
    )
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


class IdentityHash:
    digest_size = 32
    block_size = 32
    name = 'identity'

    def __init__(self, data: bytes = b'') -> None:
        self.data = bytes(data)

    def update(self, data: bytes) -> None:
        self.data += bytes(data)

    def digest(self) -> bytes:
        return self.data

    def hexdigest(self) -> str:
        return self.digest().hex()

    def copy(self) -> 'IdentityHash':
        return self.__class__(self.data)
