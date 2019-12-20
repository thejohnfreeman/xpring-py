import pytest

import xpring.codecs as codecs
from xpring.algorithms import ed25519, secp256k1

codec = codecs.DEFAULT_CODEC

ED25519_EXAMPLES = [
    # https://github.com/ripple/ripple-address-codec/blob/master/src/xrp-codec.test.ts#L74-L102
    ('4C3A1D213FBDFB14C7C28D609469B341', 'sEdTM1uX8pu2do5XvTnutH6HsouMaM2'),
    ('00000000000000000000000000000000', 'sEdSJHS4oiAdz7w2X2ni1gFiqtbJHqE'),
    ('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF', 'sEdV19BLfeQeKdEXyYA4NhjPJe6XBfG')
]

SECP256K1_EXAMPLES = [
    ('CF2DE378FBDD7E2EE87D486DFB5A7BFF', 'sn259rEFXrQrWyx3Q7XneWcwV6dfL'),
    ('00000000000000000000000000000000', 'sp6JS7f14BuwFY8Mw6bTtLKWauoUs'),
    ('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF', 'saGwBRReqUNKuWNLpUAq8i8NkXEPN')
]


@pytest.mark.parametrize('hex,encoded', ED25519_EXAMPLES)
def test_encode_ed25519_seed(hex, encoded):
    assert codec.encode_seed(bytes.fromhex(hex), ed25519) == encoded


@pytest.mark.parametrize('hex,encoded', ED25519_EXAMPLES)
def test_decode_ed25519_seed(hex, encoded):
    seed, algorithm = codec.decode_seed(encoded)
    assert algorithm == ed25519
    assert seed.hex().upper() == hex


@pytest.mark.parametrize('hex,encoded', SECP256K1_EXAMPLES)
def test_encode_secp256k1_seed(hex, encoded):
    assert codec.encode_seed(bytes.fromhex(hex), secp256k1) == encoded


@pytest.mark.parametrize('hex,encoded', SECP256K1_EXAMPLES)
def test_decode_secp256k1_seed(hex, encoded):
    seed, algorithm = codec.decode_seed(encoded)
    assert algorithm == secp256k1
    assert seed.hex().upper() == hex


def test_encode_address():
    address = bytes.fromhex('BA8E78626EE42C41B46D46C3048DF3A1C3C87072')
    encoded = 'rJrRMgiRgrU6hDF4pgu5DXQdWyPbY35ErN'
    assert codec.encode_address(address) == encoded
