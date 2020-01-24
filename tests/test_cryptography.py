import pytest

from fixtures.secp256k1 import SIGNATURE_EXAMPLES
from fixtures.packages.cryptography import make_signing_key


@pytest.mark.parametrize(*SIGNATURE_EXAMPLES)
def test_key(
    signing_key_hex: str,
    message_digest_hex: str,
    signature_hex: str,
):
    signing_key = make_signing_key(bytes.fromhex(signing_key_hex))
    assert signing_key.private_numbers()._private_value.to_bytes(
        32, 'big'
    ).hex() == signing_key_hex
