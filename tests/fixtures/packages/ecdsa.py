import hashlib
import typing as t

from ecdsa import curves, SigningKey, VerifyingKey
# The canonical signature encoding enforces low S values, by negating the value
# (modulo the order) if above order/2.
from ecdsa.util import sigdecode_der, sigencode_der_canonize

from xpring.hashes import IdentityHash


def make_signing_key(signing_key_bytes: bytes) -> SigningKey:
    return SigningKey.from_string(
        signing_key_bytes,
        curve=curves.SECP256k1,
        hashfunc=IdentityHash,
    )


def sign(signing_key: SigningKey, message_digest_bytes: bytes) -> bytes:
    return signing_key.sign_digest_deterministic(
        message_digest_bytes,
        hashfunc=hashlib.sha256,
        sigencode=sigencode_der_canonize,
    )


def derive_verifying_key(signing_key: SigningKey) -> VerifyingKey:
    return signing_key.verifying_key


def export_verifying_key(verifying_key: VerifyingKey) -> bytes:
    return verifying_key.to_pem()


def import_verifying_key(pem_bytes: bytes) -> VerifyingKey:
    return VerifyingKey.from_pem(pem_bytes)


def verify(
    verifying_key: VerifyingKey,
    message_digest_bytes: bytes,
    signature_bytes: bytes,
) -> bool:
    return verifying_key.verify(
        signature_bytes,
        message_digest_bytes,
        hashfunc=IdentityHash,
        sigdecode=sigdecode_der,
    )
