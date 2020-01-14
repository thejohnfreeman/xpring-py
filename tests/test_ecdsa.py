from ecdsa import curves, SigningKey
# The canonical signature encoding enforces low S values, by negating the value
# (modulo the order) if above order/2.
from ecdsa.util import sigencode_der, sigencode_der_canonize

from .fixtures import (
    expected_signature_hex,
    message_bytes,
    message_hash_bytes,
    NoHash,
    private_key_bytes,
)

private_key = SigningKey.from_string(
    private_key_bytes, curve=curves.SECP256k1, hashfunc=NoHash
)


def test_determinism():
    signature1_hex = private_key.sign_deterministic(message_bytes).hex()
    signature2_hex = private_key.sign_deterministic(message_bytes).hex()
    assert signature1_hex == signature2_hex


def sign(message_hash_bytes, private_key_bytes):
    private_key = SigningKey.from_string(
        private_key_bytes, curve=curves.SECP256k1, hashfunc=NoHash
    )
    return private_key.sign_deterministic(
        message_hash_bytes, hashfunc=NoHash, sigencode=sigencode_der
    )


def test_sign():
    signature = sign(message_hash_bytes, private_key_bytes)
    assert signature.hex() == expected_signature_hex
