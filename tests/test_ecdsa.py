import typing as t

from ecdsa import curves, SigningKey
# The canonical signature encoding enforces low S values, by negating the value
# (modulo the order) if above order/2.
from ecdsa.util import sigencode_der, sigencode_der_canonize

from .fixtures import IdentityHash


def make_signing_key(signing_key_bytes: bytes) -> t.Any:
    return SigningKey.from_string(
        signing_key_bytes,
        curve=curves.SECP256k1,
        hashfunc=IdentityHash,
    )


def sign(signing_key: t.Any, message_hash_bytes: bytes) -> bytes:
    return signing_key.sign_deterministic(
        message_hash_bytes,
        hashfunc=IdentityHash,
        sigencode=sigencode_der,
    )
