import typing as t

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.utils import register_interface
import pytest

from .fixtures import (
    IdentityHash,
    SECP256K1_SIGNATURE_EXAMPLES,
)

register_interface(hashes.HashAlgorithm)(IdentityHash)


def make_signing_key(signing_key_bytes: bytes) -> t.Any:
    return ec.derive_private_key(
        int.from_bytes(signing_key_bytes, byteorder='big'),
        ec.SECP256K1(),
        default_backend(),
    )


def sign(signing_key: t.Any, message_hash_bytes: bytes) -> bytes:
    prehashed = utils.Prehashed(IdentityHash())
    return signing_key.sign(message_hash_bytes, ec.ECDSA(prehashed))


@pytest.mark.parametrize(*SECP256K1_SIGNATURE_EXAMPLES)
def test_key(
    signing_key_hex: str,
    message_hash_hex: str,
    signature_hex: str,
):
    signing_key = make_signing_key(bytes.fromhex(signing_key_hex))
    assert signing_key.private_numbers()._private_value.to_bytes(
        32, 'big'
    ).hex() == signing_key_hex
