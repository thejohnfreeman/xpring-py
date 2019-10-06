import nacl.signing

from xpring import hashes
from xpring.key import Key

SEED_PREFIX = b'\x01\xE1\x4B'

KEY_PREFIX = 'ED'


def derive_key_pair(entropy: bytes) -> nacl.signing.SigningKey:
    private_key = hashes.sha512half(entropy)
    public_key = nacl.signing.SigningKey(private_key).verify_key._key[:32]  # pylint: disable=protected-access
    return (Key(public_key, KEY_PREFIX), Key(private_key, KEY_PREFIX))


def derive_address(public_key: bytes) -> str:
    pass


def sign(message: bytes, private_key: Key) -> bytes:
    key = nacl.signing.SigningKey(private_key.bytes)
    return key.sign(message, hashes.RAW_ENCODER).signature


def verify(message: bytes, signature: bytes, public_key: Key) -> bytes:
    key = nacl.signing.VerifyKey(public_key.bytes)
    return key.verify(message, signature, hashes.RAW_ENCODER) == message
