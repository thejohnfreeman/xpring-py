import nacl.signing

from xpring import hashes

SEED_PREFIX = b'\x01\xE1\x4B'

KEY_PREFIX = 'ED'


class Key:

    def __init__(self, prefix: str, attr: str, key) -> None:
        self.prefix = prefix
        self.attr = attr
        self.key = key

    def __str__(self) -> str:
        return self.prefix + getattr(self.key, self.attr)[:32].hex().upper()


def derive_key_pair(entropy: bytes) -> nacl.signing.SigningKey:
    private_key_bytes = hashes.sha512half(entropy)
    private_key = nacl.signing.SigningKey(private_key_bytes)
    public_key = private_key.verify_key
    return (
        Key(KEY_PREFIX, '_key', public_key),
        Key(KEY_PREFIX, '_signing_key', private_key),
    )


def sign(message: bytes, private_key: nacl.signing.SigningKey) -> bytes:
    return private_key.key.sign(message, hashes.RAW_ENCODER).signature


def verify(
    message: bytes, signature: bytes, public_key: nacl.signing.VerifyKey
) -> bytes:
    return public_key.key.verify(
        message, signature, hashes.RAW_ENCODER
    ) == message
