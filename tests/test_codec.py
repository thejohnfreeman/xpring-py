import pytest

import xpring.codecs as codecs

codec = codecs.Codec()


@pytest.mark.parametrize(
    'seed,encoded', [
        ('4C3A1D213FBDFB14C7C28D609469B341', 'sEdTM1uX8pu2do5XvTnutH6HsouMaM2'),
        ('00000000000000000000000000000000', 'sEdSJHS4oiAdz7w2X2ni1gFiqtbJHqE'),
        ('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF', 'sEdV19BLfeQeKdEXyYA4NhjPJe6XBfG')
    ]
)
def test_encode_ed25519_seed(seed, encoded):
    assert codec.encode_seed(seed, codecs.Encoding.ED25519) == encoded


@pytest.mark.parametrize(
    'seed,encoded', [
        ('CF2DE378FBDD7E2EE87D486DFB5A7BFF', 'sn259rEFXrQrWyx3Q7XneWcwV6dfL'),
        ('00000000000000000000000000000000', 'sp6JS7f14BuwFY8Mw6bTtLKWauoUs'),
        ('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF', 'saGwBRReqUNKuWNLpUAq8i8NkXEPN')
    ]
)
def test_encode_secp256k1_seed(seed, encoded):
    assert codec.encode_seed(seed, codecs.Encoding.SECP256K1) == encoded
