import typing as t

from fastecdsa import curve, ecdsa, keys
from fastecdsa.encoding.der import DEREncoder
from fastecdsa.encoding.pem import PEMEncoder
from fastecdsa.point import Point

from xpring.hashes import IdentityHash

SigningKey = int
VerifyingKey = Point


def make_signing_key(signing_key_bytes: bytes) -> SigningKey:
    return int.from_bytes(signing_key_bytes, byteorder='big')


def sign(signing_key: SigningKey, message_digest_bytes: bytes) -> bytes:
    r, s = ecdsa.sign(
        message_digest_bytes.hex(),
        signing_key,
        curve=curve.secp256k1,
        prehashed=True,
    )
    return DEREncoder.encode_signature(r, s)


def derive_verifying_key(signing_key: SigningKey) -> VerifyingKey:
    return keys.get_public_key(signing_key, curve.secp256k1)


def export_verifying_key(verifying_key: VerifyingKey) -> bytes:
    return PEMEncoder.encode_public_key(verifying_key).encode()


def import_verifying_key(pem_bytes: bytes) -> VerifyingKey:
    return PEMEncoder.decode_public_key(pem_bytes.decode(), curve.secp256k1)


def verify(
    verifying_key: VerifyingKey,
    message_digest_bytes: bytes,
    signature_bytes: bytes,
) -> bool:
    r, s = DEREncoder.decode_signature(signature_bytes)
    return ecdsa.verify(
        (r, s),
        message_digest_bytes,
        verifying_key,
        curve=curve.secp256k1,
        hashfunc=IdentityHash,
    )
