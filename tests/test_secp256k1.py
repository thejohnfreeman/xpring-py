import typing as t

import pytest

from .fixtures import SECP256K1_SIGNATURE_EXAMPLES
from .test_cryptography import (
    make_private_key as mpk_cryptography,
    sign as sign_cryptography,
)
from .test_ecdsa import (
    make_private_key as mpk_ecdsa,
    sign as sign_ecdsa,
)
from .test_fastecdsa import (
    make_private_key as mpk_fastecdsa,
    sign as sign_fastecdsa,
)


@pytest.mark.parametrize(*SECP256K1_SIGNATURE_EXAMPLES)
@pytest.mark.parametrize(
    'make_private_key,sign', (
        (mpk_cryptography, sign_cryptography),
        (mpk_ecdsa, sign_ecdsa),
        (mpk_fastecdsa, sign_fastecdsa),
    )
)
def test_determinism(
    private_key_hex: str,
    message_hash_hex: str,
    signature_hex: str,
    make_private_key: t.Callable[[bytes], t.Any],
    sign: t.Callable[[t.Any, bytes], bytes],
):
    private_key_bytes = bytes.fromhex(private_key_hex)
    private_key = make_private_key(private_key_bytes)
    message_hash_bytes = bytes.fromhex(message_hash_hex)
    signature1_hex = sign(private_key, message_hash_bytes).hex()
    signature2_hex = sign(private_key, message_hash_bytes).hex()
    assert signature1_hex == signature2_hex


@pytest.mark.parametrize(*SECP256K1_SIGNATURE_EXAMPLES)
@pytest.mark.parametrize(
    'make_private_key,sign', (
        (mpk_cryptography, sign_cryptography),
        (mpk_ecdsa, sign_ecdsa),
        (mpk_fastecdsa, sign_fastecdsa),
    )
)
def test_sign(
    private_key_hex: str,
    message_hash_hex: str,
    signature_hex: str,
    make_private_key: t.Callable[[bytes], t.Any],
    sign: t.Callable[[t.Any, bytes], bytes],
):
    private_key_bytes = bytes.fromhex(private_key_hex)
    private_key = make_private_key(private_key_bytes)
    message_hash_bytes = bytes.fromhex(message_hash_hex)
    signature_bytes = sign(private_key, message_hash_bytes)
    assert signature_bytes.hex() == signature_hex
