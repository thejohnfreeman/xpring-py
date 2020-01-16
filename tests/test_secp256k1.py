import typing as t

import pytest

from .fixtures import SECP256K1_SIGNATURE_EXAMPLES
from . import test_cryptography
from . import test_ecdsa
from . import test_fastecdsa

SECP256K1_LIBRARY_EXAMPLES = (
    pytest.param(test_cryptography, id='cryptography'),
    pytest.param(test_ecdsa, id='ecdsa'),
    pytest.param(test_fastecdsa, id='fastecdsa'),
)


@pytest.mark.parametrize(*SECP256K1_SIGNATURE_EXAMPLES)
@pytest.mark.parametrize('module', SECP256K1_LIBRARY_EXAMPLES)
def test_determinism(
    signing_key_hex: str,
    message_hash_hex: str,
    signature_hex: str,
    module: t.Any,
):
    signing_key_bytes = bytes.fromhex(signing_key_hex)
    signing_key = module.make_signing_key(signing_key_bytes)
    message_hash_bytes = bytes.fromhex(message_hash_hex)
    signature1_hex = module.sign(signing_key, message_hash_bytes).hex()
    signature2_hex = module.sign(signing_key, message_hash_bytes).hex()
    assert signature1_hex == signature2_hex


@pytest.mark.skip
@pytest.mark.parametrize(*SECP256K1_SIGNATURE_EXAMPLES)
@pytest.mark.parametrize('module', SECP256K1_LIBRARY_EXAMPLES)
def test_sign(
    signing_key_hex: str,
    message_hash_hex: str,
    signature_hex: str,
    module: t.Any,
):
    signing_key_bytes = bytes.fromhex(signing_key_hex)
    signing_key = module.make_signing_key(signing_key_bytes)
    message_hash_bytes = bytes.fromhex(message_hash_hex)
    signature_bytes = module.sign(signing_key, message_hash_bytes)
    assert signature_bytes.hex() == signature_hex
