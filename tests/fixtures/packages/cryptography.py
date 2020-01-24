import typing as t

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.utils import register_interface
import pytest

from xpring.hashes import IdentityHash

register_interface(hashes.HashAlgorithm)(IdentityHash)


def make_signing_key(signing_key_bytes: bytes) -> t.Any:
    return ec.derive_private_key(
        int.from_bytes(signing_key_bytes, byteorder='big'),
        ec.SECP256K1(),
        default_backend(),
    )


def sign(signing_key: t.Any, digest_bytes: bytes) -> bytes:
    # https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ec/#elliptic-curve-signature-algorithms
    prehashed = utils.Prehashed(IdentityHash())
    return signing_key.sign(digest_bytes, ec.ECDSA(prehashed))


def derive_verifying_key(signing_key: t.Any) -> t.Any:
    return signing_key.public_key()


def export_verifying_key(verifying_key: t.Any) -> bytes:
    # https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ec/#serialization
    return verifying_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def import_verifying_key(pem: bytes) -> t.Any:
    # https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ec/#key-loading
    return serialization.load_pem_public_key(pem, backend=default_backend())


def verify(verifying_key: t.Any, digest_bytes: bytes, signature: bytes) -> bool:
    # https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ec/#elliptic-curve-signature-algorithms
    verifying_key.verify(
        signature,
        digest_bytes,
        ec.ECDSA(utils.Prehashed(IdentityHash())),
    )
    return True
