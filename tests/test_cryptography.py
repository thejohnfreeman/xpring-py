from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.utils import register_interface
import pytest
import typing as t

from .fixtures import (
    IdentityHash,
    MessageHashHex,
    PrivateKeyHex,
    SECP256K1_SIGNATURE_EXAMPLES,
    SignatureHex,
)

register_interface(hashes.HashAlgorithm)(IdentityHash)

PrivateKey = t.Any


def make_private_key(private_key_hex: PrivateKeyHex) -> PrivateKey:
    return ec.derive_private_key(
        int.from_bytes(bytes.fromhex(private_key_hex), byteorder='big'),
        ec.SECP256K1(),
        default_backend(),
    )


def sign(
    private_key: PrivateKey, message_hash_hex: MessageHashHex
) -> SignatureHex:
    message_hash_bytes = bytes.fromhex(message_hash_hex)
    prehashed = utils.Prehashed(IdentityHash())
    return private_key.sign(message_hash_bytes, ec.ECDSA(prehashed)).hex()


@pytest.mark.parametrize(*SECP256K1_SIGNATURE_EXAMPLES)
def test_key(
    private_key_hex: PrivateKeyHex,
    message_hash_hex: MessageHashHex,
    signature_hex: SignatureHex,
):
    private_key = make_private_key(private_key_hex)
    assert private_key.private_numbers()._private_value.to_bytes(
        32, 'big'
    ).hex() == private_key_hex


@pytest.mark.parametrize(*SECP256K1_SIGNATURE_EXAMPLES)
def test_sign(
    private_key_hex: PrivateKeyHex,
    message_hash_hex: MessageHashHex,
    signature_hex: SignatureHex,
):
    private_key = make_private_key(private_key_hex)
    assert sign(private_key, message_hash_hex) == signature_hex
