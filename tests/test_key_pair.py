import pytest

from xpring.key_pair import KeyPair


def test_ed25519_key_pair():
    seed = 'sEdSKaCy2JT7JaM7v95H9SxkhP9wS2r'
    key_pair = KeyPair.from_seed(seed)
    assert str(
        key_pair.public_key
    ) == 'ED01FA53FA5A7E77798F882ECE20B1ABC00BB358A9E55A202D0D0676BD0CE37A63'
    assert str(
        key_pair.private_key
    ) == 'EDB4C4E046826BD26190D09715FC31F4E6A728204EADD112905B08B14B7F15C4F3'


def test_ed25519_address():
    seed = 'sEdSKaCy2JT7JaM7v95H9SxkhP9wS2r'
    key_pair = KeyPair.from_seed(seed)
    assert str(key_pair.address) == 'rLUEXYuLiQptky37CqLcm9USQpPiz5rkpD'


@pytest.mark.skip
def test_secp256k1_address():
    seed = 'snAdZ43KgWZsNdDdbWqUDvAudLvNj'
    key_pair = KeyPair.from_seed(seed)
    assert str(key_pair.address) == 'rMMFhmCU9mzFZiNWp2dewd1dieoywGkyVk'
