import typing as t

import pytest

from .fixtures import SECP256K1_SIGNATURE_EXAMPLES
from . import cryptography
from . import ecdsa
from . import fastecdsa

SECP256K1_LIBRARY_EXAMPLES = (
    pytest.param(cryptography, id='cryptography'),
    pytest.param(ecdsa, id='ecdsa'),
    pytest.param(fastecdsa, id='fastecdsa'),
)


@pytest.mark.parametrize(*SECP256K1_SIGNATURE_EXAMPLES)
@pytest.mark.parametrize('module', SECP256K1_LIBRARY_EXAMPLES)
def test_determinism(
    signing_key_hex: str,
    message_digest_hex: str,
    signature_hex: str,
    module: t.Any,
):
    # This package offers no deterministic signing algorithm.
    if module == cryptography:
        return

    signing_key_bytes = bytes.fromhex(signing_key_hex)
    signing_key = module.make_signing_key(signing_key_bytes)
    digest_bytes = bytes.fromhex(message_digest_hex)
    signature1_hex = module.sign(signing_key, digest_bytes).hex()
    signature2_hex = module.sign(signing_key, digest_bytes).hex()
    assert signature1_hex == signature2_hex


# It is not possible in general to replicate signatures because they may have
# been generated using a random nonce (named `k`).
# In general, it is only possible to verify signatures.
# test_verify checks that each library can verify known good signatures.
# test_agreement checks that each library can verify every library's
# signatures, including its own.


@pytest.mark.parametrize(*SECP256K1_SIGNATURE_EXAMPLES)
@pytest.mark.parametrize('module', SECP256K1_LIBRARY_EXAMPLES)
def test_verify(
    signing_key_hex: str,
    message_digest_hex: str,
    signature_hex: str,
    module: t.Any,
):
    """Verify known good signatures."""
    signing_key_bytes = bytes.fromhex(signing_key_hex)
    signing_key = module.make_signing_key(signing_key_bytes)
    verifying_key = module.derive_verifying_key(signing_key)
    digest_bytes = bytes.fromhex(message_digest_hex)
    signature_bytes = bytes.fromhex(signature_hex)
    assert module.verify(verifying_key, digest_bytes, signature_bytes)


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
    signing_key_bytes = bytes.fromhex(signing_key_hex)
    signing_key1 = module1.make_signing_key(signing_key_bytes)
    verifying_key1 = module1.derive_verifying_key(signing_key1)
    pem1 = module1.export_verifying_key(verifying_key1)
    digest_bytes = bytes.fromhex(message_digest_hex)
    signature_bytes1 = module1.sign(signing_key1, digest_bytes)

    verifying_key2 = module2.import_verifying_key(pem1)
    assert module2.verify(verifying_key2, digest_bytes, signature_bytes1)
