import pytest

from xpring.key_pair import KeyPair


# https://github.com/ripple/ripple-keypairs/blob/6f606a885ae5cb2e897c796c98171938aba19903/test/fixtures/api.json#L12-L21
def test_ed25519_key_pair():
    encoded_seed = 'sEdSKaCy2JT7JaM7v95H9SxkhP9wS2r'
    key_pair = KeyPair.from_encoded_seed(encoded_seed)
    assert key_pair.public_key.hex().upper(
    ) == '01FA53FA5A7E77798F882ECE20B1ABC00BB358A9E55A202D0D0676BD0CE37A63'
    assert key_pair.private_key.hex().upper(
    ) == 'B4C4E046826BD26190D09715FC31F4E6A728204EADD112905B08B14B7F15C4F3'


@pytest.mark.skip
def test_ed25519_address():
    encoded_seed = 'sEdSKaCy2JT7JaM7v95H9SxkhP9wS2r'
    key_pair = KeyPair.from_encoded_seed(encoded_seed)
    assert key_pair.address == 'rLUEXYuLiQptky37CqLcm9USQpPiz5rkpD'


@pytest.mark.skip
def test_secp256k1_address():
    encoded_seed = 'snAdZ43KgWZsNdDdbWqUDvAudLvNj'
    key_pair = KeyPair.from_encoded_seed(encoded_seed)
    assert key_pair.address == 'rMMFhmCU9mzFZiNWp2dewd1dieoywGkyVk'
