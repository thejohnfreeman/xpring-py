import typing as t

from ecdsa import curves, SigningKey, VerifyingKey
# The canonical signature encoding enforces low S values, by negating the value
# (modulo the order) if above order/2.
from ecdsa.util import sigdecode_der, sigencode_der_canonize

from .fixtures import IdentityHash


def make_signing_key(signing_key_bytes: bytes) -> t.Any:
    return SigningKey.from_string(
        signing_key_bytes,
        curve=curves.SECP256k1,
        hashfunc=IdentityHash,
    )


def sign(signing_key: t.Any, digest_bytes: bytes) -> bytes:
    return signing_key.sign_deterministic(
        digest_bytes,
        hashfunc=IdentityHash,
        sigencode=sigencode_der_canonize,
    )


def derive_verifying_key(signing_key: t.Any) -> t.Any:
    return signing_key.verifying_key


def export_verifying_key(verifying_key: t.Any) -> bytes:
    return verifying_key.to_pem()


def import_verifying_key(pem_bytes: bytes) -> t.Any:
    return VerifyingKey.from_pem(pem_bytes)


def verify(verifying_key: t.Any, digest_bytes: bytes, signature: bytes) -> bool:
    return verifying_key.verify(
        signature, digest_bytes, hashfunc=IdentityHash, sigdecode=sigdecode_der
    )
