from dataclasses import dataclass
import pytest

from xpring.key_pair import KeyPair
from xpring.types import Address, EncodedSeed, PrivateKey, PublicKey

# https://github.com/ripple/ripple-keypairs/blob/6f606a885ae5cb2e897c796c98171938aba19903/test/fixtures/api.json#L12-L21
KEY_PAIR_EXAMPLES = (
    ('encoded_seed', 'private_key_hex', 'public_key_hex', 'address'), (
        (
            'sEdSKaCy2JT7JaM7v95H9SxkhP9wS2r',
            'b4c4e046826bd26190d09715fc31f4e6a728204eadd112905b08b14b7f15c4f3',
            'ed01fa53fa5a7e77798f882ece20b1abc00bb358a9e55a202d0d0676bd0ce37a63',
            'rLUEXYuLiQptky37CqLcm9USQpPiz5rkpD',
        ),
        (
            'sp5fghtJtpUorTwvof1NpDXAzNwf5',
            'd78b9735c3f26501c7337b8a5727fd53a6efdbc6aa55984f098488561f985e23',
            '030d58eb48b4420b1f7b9df55087e0e29fef0e8468f9a6825b01ca2c361042d435',
            'rU6K7V3Po4snVhBBaU29sesqs2qTQJWDw1',
        ),
    )
)


@pytest.mark.parametrize(*KEY_PAIR_EXAMPLES)
def test_private_key(
    encoded_seed: EncodedSeed,
    private_key_hex: str,
    public_key_hex: str,
    address: Address,
):
    key_pair = KeyPair.from_encoded_seed(encoded_seed)
    assert key_pair.private_key.hex() == private_key_hex


@pytest.mark.parametrize(*KEY_PAIR_EXAMPLES)
def test_public_key(
    encoded_seed: EncodedSeed,
    private_key_hex: str,
    public_key_hex: str,
    address: Address,
):
    key_pair = KeyPair.from_encoded_seed(encoded_seed)
    assert key_pair.public_key.hex() == public_key_hex


@pytest.mark.parametrize(*KEY_PAIR_EXAMPLES)
def test_address(
    encoded_seed: EncodedSeed,
    private_key_hex: str,
    public_key_hex: str,
    address: Address,
):
    key_pair = KeyPair.from_encoded_seed(encoded_seed)
    assert key_pair.address == address


@pytest.mark.parametrize(*KEY_PAIR_EXAMPLES)
def test_sign_verify(
    encoded_seed: EncodedSeed,
    private_key_hex: str,
    public_key_hex: str,
    address: Address,
):
    key_pair = KeyPair.from_encoded_seed(encoded_seed)
    message = b'message'
    signature = key_pair.sign(message)
    assert key_pair.verify(message, signature)
