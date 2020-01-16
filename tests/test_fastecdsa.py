import typing as t

from fastecdsa import curve, ecdsa
from fastecdsa.encoding.der import DEREncoder


def make_signing_key(signing_key_bytes: bytes) -> t.Any:
    return int.from_bytes(signing_key_bytes, byteorder='big')


def sign(signing_key: t.Any, message_hash_bytes: bytes) -> bytes:
    r, s = ecdsa.sign(
        message_hash_bytes.hex(),
        signing_key,
        curve=curve.secp256k1,
        prehashed=True,
    )
    return DEREncoder.encode_signature(r, s)
