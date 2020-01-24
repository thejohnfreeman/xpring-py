import nacl.signing
import pytest

from fixtures.ed25519 import SIGNATURE_EXAMPLES


@pytest.mark.parametrize(*SIGNATURE_EXAMPLES)
def test_sign(
    signing_key_hex: str,
    message_hex: str,
    signature_hex: str,
):
    signing_key_bytes = bytes.fromhex(signing_key_hex)
    assert len(signing_key_bytes) == 32
    signing_key = nacl.signing.SigningKey(signing_key_bytes)
    signature = signing_key.sign(bytes.fromhex(message_hex)).signature
    assert signature.hex() == signature_hex
