import typing as t

import nacl.encoding
import nacl.signing

from xpring import hashes, key as xk

SEED_PREFIX = b'\x01\xE1\x4B'

KEY_PREFIX = 'ED'


def derive_key_pair(entropy: bytes) -> xk.KeyPair:
    private_key = hashes.sha512half(entropy)
    public_key = nacl.signing.SigningKey(private_key).verify_key._key[:32]  # pylint: disable=protected-access
    return (xk.Key(public_key, KEY_PREFIX), xk.Key(private_key, KEY_PREFIX))


def derive_address(public_key: bytes) -> str:
    pass


def sign(message: bytes, private_key: xk.Key) -> bytes:
    key = nacl.signing.SigningKey(private_key.bytes)
    return key.sign(message, nacl.encoding.RawEncoder).signature


def verify(message: bytes, signature: bytes, public_key: xk.Key) -> bytes:
    key = nacl.signing.VerifyKey(public_key.bytes)
    return key.verify(message, signature, nacl.encoding.RawEncoder)
