from ecdsa import curves, SigningKey
# The canonical signature encoding enforces low S values, by negating the value
# (modulo the order) if above order/2.
from ecdsa.util import sigencode_der, sigencode_der_canonize
import pytest
import typing as t

from .fixtures import (
    IdentityHash,
    MessageHashHex,
    PrivateKeyHex,
    SECP256K1_SIGNATURE_EXAMPLES,
    SignatureHex,
)

# https://github.com/python/mypy/issues/7866
PrivateKey = t.Union[SigningKey]


def make_private_key(private_key_hex: PrivateKeyHex) -> PrivateKey:
    return SigningKey.from_string(
        bytes.fromhex(private_key_hex),
        curve=curves.SECP256k1,
        hashfunc=IdentityHash,
    )


def sign(
    private_key: PrivateKey, message_hash_hex: MessageHashHex
) -> SignatureHex:
    return private_key.sign_deterministic(
        bytes.fromhex(message_hash_hex),
        hashfunc=IdentityHash,
        sigencode=sigencode_der,
    ).hex()


@pytest.mark.parametrize(*SECP256K1_SIGNATURE_EXAMPLES)
def test_determinism(
    private_key_hex: PrivateKeyHex,
    message_hash_hex: MessageHashHex,
    signature_hex: SignatureHex,
):
    private_key = make_private_key(private_key_hex)
    signature1_hex = sign(private_key, message_hash_hex)
    signature2_hex = sign(private_key, message_hash_hex)
    assert signature1_hex == signature2_hex


@pytest.mark.parametrize(*SECP256K1_SIGNATURE_EXAMPLES)
def test_sign(
    private_key_hex: PrivateKeyHex,
    message_hash_hex: MessageHashHex,
    signature_hex: SignatureHex,
):
    private_key = make_private_key(private_key_hex)
    assert sign(private_key, message_hash_hex) == signature_hex
