import typing as t

from fastecdsa import curve, ecdsa
import pytest

from .fixtures import (
    MessageHashHex,
    PrivateKeyHex,
    SECP256K1_SIGNATURE_EXAMPLES,
    SignatureHex,
)


def encode_der(r: int, s: int) -> bytes:
    assert r < (1 << (32 * 8))
    assert s < (1 << (32 * 8))
    # If r and s are 32-byte integers, the DER encoding is:
    # 1-byte code for SEQUENCE (0x30) +
    # 1-byte length of sequence (0x01 + 0x01 + 0x20 + 0x01 + 0x01 + 0x20 = 0x44) +
    # 1-byte code for INTEGER (0x02) + 1-byte for length of r (0x20) + r
    # 1-byte code for INTEGER (0x02) + 1-byte for length of s (0x20) + s
    # https://docs.microsoft.com/en-us/windows/win32/seccertenroll/about-introduction-to-asn-1-syntax-and-encoding
    r_bytes = r.to_bytes(32, byteorder='big')
    s_bytes = s.to_bytes(32, byteorder='big')
    return b'\x30\x44' + b'\x02\x20' + r_bytes + b'\x02\x20' + s_bytes


PrivateKey = t.NewType('PrivateKey', int)


def make_private_key(private_key_hex: PrivateKeyHex) -> PrivateKey:
    return t.cast(
        PrivateKey,
        int.from_bytes(bytes.fromhex(private_key_hex), byteorder='big'),
    )


def sign(
    private_key: PrivateKey, message_hash_hex: MessageHashHex
) -> SignatureHex:
    r, s = ecdsa.sign(
        message_hash_hex, private_key, curve=curve.secp256k1, prehashed=True
    )
    return t.cast(SignatureHex, encode_der(r, s).hex())


@pytest.mark.parametrize(*SECP256K1_SIGNATURE_EXAMPLES)
def test_determinism(
    private_key_hex: PrivateKeyHex,
    message_hash_hex: MessageHashHex,
    signature_hex: SignatureHex,
):
    private_key = make_private_key(private_key_hex)
    signature1_hex = sign(private_key, message_hash_hex)
    signature2_hex = sign(private_key, message_hash_hex)
    assert signature1_hex == signature2_hex


@pytest.mark.parametrize(*SECP256K1_SIGNATURE_EXAMPLES)
def test_sign(
    private_key_hex: PrivateKeyHex,
    message_hash_hex: MessageHashHex,
    signature_hex: SignatureHex,
):
    private_key = make_private_key(private_key_hex)
    assert sign(private_key, message_hash_hex) == signature_hex
