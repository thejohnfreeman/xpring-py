from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.utils import register_interface

from .fixtures import (
    expected_signature_hex,
    message_bytes,
    message_hash_bytes,
    IdentityHash,
    private_key_bytes,
)

register_interface(hashes.HashAlgorithm)(IdentityHash)


def test_key():
    private_key = ec.derive_private_key(
        int.from_bytes(private_key_bytes, byteorder='big'),
        ec.SECP256K1(),
        default_backend(),
    )
    private_key_hex = private_key.private_numbers()._private_value.to_bytes(
        32, 'big'
    ).hex()
    assert private_key_hex == private_key_bytes.hex()


def sign(message_hash_bytes, private_key_bytes):
    private_key = ec.derive_private_key(
        int.from_bytes(private_key_bytes, byteorder='big'),
        ec.SECP256K1(),
        default_backend(),
    )
    prehashed = utils.Prehashed(IdentityHash())
    return private_key.sign(message_hash_bytes, ec.ECDSA(prehashed))


def test_sign():
    signature = sign(message_hash_bytes, private_key_bytes)
    assert signature.hex() == expected_signature_hex
