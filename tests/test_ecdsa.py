from fastecdsa import curve, ecdsa
import pytest

from xpring import hashes


def encode_der(r: int, s: int) -> str:
    # If r and s are 32 bytes, the DER encoding is:
    # 1 byte code for SEQUENCE (0x30) +
    # 1 byte length of sequence (0x01 + 0x01 + 0x20 + 0x01 + 0x01 + 0x20 = 0x44) +
    # 1 byte code for INTEGER (0x02) + 1 byte for length of r (0x20) + r
    # 1 byte code for INTEGER (0x02) + 1 byte for length of s (0x20) + s
    # https://docs.microsoft.com/en-us/windows/win32/seccertenroll/about-introduction-to-asn-1-syntax-and-encoding
    r = r.to_bytes(32, byteorder='big').hex()
    s = s.to_bytes(32, byteorder='big').hex()
    return '3044' + '0220' + r + '0220' + s


def test_ecdsa_sign():
    # Example key, message, and signature (i.e. the test vector) come from here:
    # https://github.com/ripple/ripple-keypairs/blob/master/test/fixtures/api.json#L2-L11
    private_key_bytes = bytes.fromhex(
        'd78b9735c3f26501c7337b8a5727fd53a6efdbc6aa55984f098488561f985e23'
    )
    message_hash_bytes = hashes.sha512half(b'test message')
    assert message_hash_bytes.hex(
    ) == '950b2a7effa78f51a63515ec45e03ecebe50ef2f1c41e69629b50778f11bc080'
    r, s = ecdsa.sign(
        message_hash_bytes.hex(),
        int.from_bytes(private_key_bytes, byteorder='big'),
        curve=curve.secp256k1,
        prehashed=True
    )
    expected_signature_hex = '30440220583a91c95e54e6a651c47bec22744e0b101e2c4060e7b08f6341657dad9bc3ee02207d1489c7395db0188d3a56a977ecba54b36fa9371b40319655b1b4429e33ef2d'
    assert encode_der(r, s) == expected_signature_hex
