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
    message_digest_hex: str,
    signature_hex: str,
    module: t.Any,
):
    signing_key_bytes = bytes.fromhex(signing_key_hex)
    signing_key = module.make_signing_key(signing_key_bytes)
    message_digest_bytes = bytes.fromhex(message_digest_hex)
    signature1_hex = module.sign(signing_key, message_digest_bytes).hex()
    signature2_hex = module.sign(signing_key, message_digest_bytes).hex()
    assert signature1_hex == signature2_hex


@pytest.mark.parametrize(*SECP256K1_SIGNATURE_EXAMPLES)
@pytest.mark.parametrize('module', SECP256K1_LIBRARY_EXAMPLES)
def test_verify(
    signing_key_hex: str,
    message_digest_hex: str,
    signature_hex: str,
    module: t.Any,
):
    """Verify known good signatures."""
    if (
        not hasattr(module, 'derive_verifying_key') or
        not hasattr(module, 'verify')
    ):
        return

    signing_key_bytes = bytes.fromhex(signing_key_hex)
    signing_key = module.make_signing_key(signing_key_bytes)
    verifying_key = module.derive_verifying_key(signing_key)
    message_digest_bytes = bytes.fromhex(message_digest_hex)
    signature_bytes = bytes.fromhex(signature_hex)
    assert module.verify(verifying_key, message_digest_bytes, signature_bytes)


@pytest.mark.skip
@pytest.mark.parametrize(*SECP256K1_SIGNATURE_EXAMPLES)
@pytest.mark.parametrize('module', SECP256K1_LIBRARY_EXAMPLES)
def test_sign(
    signing_key_hex: str,
    message_digest_hex: str,
    signature_hex: str,
    module: t.Any,
):
    """Replicate the signatures from the test vectors.

    This is not possible in general because the signature may have been
    computed using a random nonce named `k`.
    """
    signing_key_bytes = bytes.fromhex(signing_key_hex)
    signing_key = module.make_signing_key(signing_key_bytes)
    message_digest_bytes = bytes.fromhex(message_digest_hex)
    signature_bytes = module.sign(signing_key, message_digest_bytes)
    assert signature_bytes.hex() == signature_hex


@pytest.mark.skip
@pytest.mark.parametrize(*SECP256K1_SIGNATURE_EXAMPLES)
@pytest.mark.parametrize('module1', SECP256K1_LIBRARY_EXAMPLES)
@pytest.mark.parametrize('module2', SECP256K1_LIBRARY_EXAMPLES)
def test_agreement(
    signing_key_hex: str,
    message_digest_hex: str,
    signature_hex: str,
    module1: t.Any,
    module2: t.Any,
):
    if (
        not hasattr(module1, 'derive_verifying_key') or
        not hasattr(module2, 'verify')
    ):
        return

    signing_key_bytes = bytes.fromhex(signing_key_hex)
    signing_key1 = module1.make_signing_key(signing_key_bytes)
    verifying_key1 = module1.derive_verifying_key(signing_key1)
    message_digest_bytes = bytes.fromhex(message_digest_hex)
    signature_bytes1 = module1.sign(signing_key1, message_digest_bytes)

    assert module2.verify(
        verifying_key1, message_digest_bytes, signature_bytes1
    )
