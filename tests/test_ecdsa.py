from ecdsa import curves, SigningKey
# The canonical signature encoding enforces low S values, by negating the value
# (modulo the order) if above order/2.
from ecdsa.util import sigencode_der, sigencode_der_canonize
import pytest

from .fixtures import (
    IdentityHash,
    SECP256K1_SIGNATURE_EXAMPLES,
)


@pytest.mark.parametrize(*SECP256K1_SIGNATURE_EXAMPLES)
def test_determinism(
    private_key_bytes: bytes, message_hash_bytes: bytes, signature_bytes: bytes
):
    private_key = SigningKey.from_string(
        private_key_bytes, curve=curves.SECP256k1, hashfunc=IdentityHash
    )
    message_bytes = b'message'
    signature1_hex = private_key.sign_deterministic(message_bytes).hex()
    signature2_hex = private_key.sign_deterministic(message_bytes).hex()
    assert signature1_hex == signature2_hex


def sign(message_hash_bytes, private_key_bytes):
    private_key = SigningKey.from_string(
        private_key_bytes, curve=curves.SECP256k1, hashfunc=IdentityHash
    )
    return private_key.sign_deterministic(
        message_hash_bytes, hashfunc=IdentityHash, sigencode=sigencode_der
    )


@pytest.mark.parametrize(*SECP256K1_SIGNATURE_EXAMPLES)
def test_sign(
    private_key_bytes: bytes, message_hash_bytes: bytes, signature_bytes: bytes
):
    assert sign(message_hash_bytes, private_key_bytes) == signature_bytes
