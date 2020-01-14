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


@pytest.mark.parametrize(*SECP256K1_SIGNATURE_EXAMPLES)
def test_key(
    private_key_bytes: bytes, message_hash_bytes: bytes, signature_bytes: bytes
):
    private_key = ec.derive_private_key(
        int.from_bytes(private_key_bytes, byteorder='big'),
        ec.SECP256K1(),
        default_backend(),
    )
    private_key_hex = private_key.private_numbers()._private_value.to_bytes(
        32, 'big'
    ).hex()
    assert private_key_hex == private_key_bytes.hex()


def sign(message_hash_bytes: bytes, private_key_bytes: bytes) -> bytes:
    private_key = ec.derive_private_key(
        int.from_bytes(private_key_bytes, byteorder='big'),
        ec.SECP256K1(),
        default_backend(),
    )
    prehashed = utils.Prehashed(IdentityHash())
    return private_key.sign(message_hash_bytes, ec.ECDSA(prehashed))


@pytest.mark.parametrize(*SECP256K1_SIGNATURE_EXAMPLES)
def test_sign(
    private_key_bytes: bytes, message_hash_bytes: bytes, signature_bytes: bytes
):
    assert sign(message_hash_bytes, private_key_bytes) == signature_bytes
