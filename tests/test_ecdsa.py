from ecdsa import curves, SigningKey
# The canonical signature encoding enforces low S values, by negating the value
# (modulo the order) if above order/2.
from ecdsa.util import sigencode_der, sigencode_der_canonize

from .signing import (
    expected_signature_hex,
    message_bytes,
    message_hash_bytes,
    NoHash,
    private_key_bytes,
)


def test_determinism():
    private_key = SigningKey.from_string(
        private_key_bytes, curve=curves.SECP256k1, hashfunc=NoHash
    )
    signature1_hex = private_key.sign_deterministic(message_bytes).hex()
    signature2_hex = private_key.sign_deterministic(message_bytes).hex()
    assert signature1_hex == signature2_hex


def test_sign():
    private_key = SigningKey.from_string(
        private_key_bytes, curve=curves.SECP256k1, hashfunc=NoHash
    )
    signature = private_key.sign_deterministic(
        message_hash_bytes, hashfunc=NoHash, sigencode=sigencode_der
    )
    assert signature.hex() == expected_signature_hex
