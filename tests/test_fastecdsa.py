import pytest

from fastecdsa import curve, ecdsa

from .signing import (
    expected_signature_hex,
    message_hash_bytes,
    private_key_bytes,
)


def encode_der(r: int, s: int) -> str:
    # If r and s are 32-byte integers, the DER encoding is:
    # 1-byte code for SEQUENCE (0x30) +
    # 1-byte length of sequence (0x01 + 0x01 + 0x20 + 0x01 + 0x01 + 0x20 = 0x44) +
    # 1-byte code for INTEGER (0x02) + 1-byte for length of r (0x20) + r
    # 1-byte code for INTEGER (0x02) + 1-byte for length of s (0x20) + s
    # https://docs.microsoft.com/en-us/windows/win32/seccertenroll/about-introduction-to-asn-1-syntax-and-encoding
    r = r.to_bytes(32, byteorder='big').hex()
    s = s.to_bytes(32, byteorder='big').hex()
    return '3044' + '0220' + r + '0220' + s


def test_determinism():
    r1, s1 = ecdsa.sign(
        message_hash_bytes.hex(),
        int.from_bytes(private_key_bytes, byteorder='big'),
        curve=curve.secp256k1,
        prehashed=True
    )
    r2, s2 = ecdsa.sign(
        message_hash_bytes.hex(),
        int.from_bytes(private_key_bytes, byteorder='big'),
        curve=curve.secp256k1,
        prehashed=True
    )
    assert r1 == r2
    assert s1 == s2


def test_sign():
    r, s = ecdsa.sign(
        message_hash_bytes.hex(),
        int.from_bytes(private_key_bytes, byteorder='big'),
        curve=curve.secp256k1,
        prehashed=True
    )
    assert encode_der(r, s) == expected_signature_hex
