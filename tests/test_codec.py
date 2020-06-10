import pytest

from xpring.codec import DEFAULT_CODEC as codec
from xpring.algorithms import ed25519, secp256k1
from xpring.key_pair import derive_account_id


@pytest.mark.parametrize(
    ('bites', 'encoded_bites'), (
        (b'\0\0\0\0', 'rrrr'),
        (b'\0\0\0\x01', 'rrrp'),
        (b'\x01', 'p'),
    )
)
def test_encode(bites, encoded_bites):
    assert codec.encode(bites) == encoded_bites


CHECKSUM_EXAMPLES = (
    ('bites', 'encoded_bites'),
    (
        # https://github.com/ripple/ripple-address-codec/blob/master/src/xrp-codec.test.ts#L156-L161
        (b'\x00123456789', 'rnaC7gW34M77Kneb78s'),
    )
)


@pytest.mark.parametrize(*CHECKSUM_EXAMPLES)
def test_encode_with_checksum(bites, encoded_bites):
    assert codec.encode_with_checksum(bites) == encoded_bites


@pytest.mark.parametrize(*CHECKSUM_EXAMPLES)
def test_decode_with_checksum(bites, encoded_bites):
    assert codec.decode_with_checksum(encoded_bites) == bites


# https://github.com/ripple/ripple-address-codec/blob/4f87237b5429a044de2c8fa369d1c45ed3210538/src/xrp-codec.test.ts#L74-L102
ED25519_SEED_EXAMPLES = (
    ('seed_hex', 'encoded_seed'), (
        ('4C3A1D213FBDFB14C7C28D609469B341', 'sEdTM1uX8pu2do5XvTnutH6HsouMaM2'),
        ('00000000000000000000000000000000', 'sEdSJHS4oiAdz7w2X2ni1gFiqtbJHqE'),
        ('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF', 'sEdV19BLfeQeKdEXyYA4NhjPJe6XBfG'),
    )
)

SECP256K1_SEED_EXAMPLES = (
    ('seed_hex', 'encoded_seed'), (
        ('CF2DE378FBDD7E2EE87D486DFB5A7BFF', 'sn259rEFXrQrWyx3Q7XneWcwV6dfL'),
        ('00000000000000000000000000000000', 'sp6JS7f14BuwFY8Mw6bTtLKWauoUs'),
        ('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF', 'saGwBRReqUNKuWNLpUAq8i8NkXEPN'),
    )
)


@pytest.mark.parametrize(*ED25519_SEED_EXAMPLES)
def test_encode_ed25519_seed(seed_hex, encoded_seed):
    seed = bytes.fromhex(seed_hex)
    assert codec.encode_seed(seed, ed25519) == encoded_seed


@pytest.mark.parametrize(*ED25519_SEED_EXAMPLES)
def test_decode_ed25519_seed(seed_hex, encoded_seed):
    seed, algorithm = codec.decode_seed(encoded_seed)
    assert algorithm == ed25519
    assert seed.hex().upper() == seed_hex


@pytest.mark.parametrize(*SECP256K1_SEED_EXAMPLES)
def test_encode_secp256k1_seed(seed_hex, encoded_seed):
    seed = bytes.fromhex(seed_hex)
    assert codec.encode_seed(seed, secp256k1) == encoded_seed


@pytest.mark.parametrize(*SECP256K1_SEED_EXAMPLES)
def test_decode_secp256k1_seed(seed_hex, encoded_seed):
    seed, algorithm = codec.decode_seed(encoded_seed)
    assert algorithm == secp256k1
    assert seed.hex().upper() == seed_hex


ADDRESS_EXAMPLES = (
    ('account_id_hex', 'address'),
    [
        # https://github.com/ripple/ripple-address-codec/blob/4f87237b5429a044de2c8fa369d1c45ed3210538/src/xrp-codec.test.ts#L30-L31
        (
            'BA8E78626EE42C41B46D46C3048DF3A1C3C87072',
            'rJrRMgiRgrU6hDF4pgu5DXQdWyPbY35ErN'
        ),
        (
            '01156D8C127623E3C55BCF1AE0A2E27E472D1749',
            'rajMp5xCrc8DqNivrxftgWfnWFLSgDYHP'
        ),
    ]
)


@pytest.mark.parametrize(*ADDRESS_EXAMPLES)
def test_encode_address(account_id_hex, address):
    account_id = bytes.fromhex(account_id_hex)
    assert codec.encode_address(account_id) == address


@pytest.mark.parametrize(*ADDRESS_EXAMPLES)
def test_decode_address(account_id_hex, address):
    account_id = bytes.fromhex(account_id_hex)
    assert codec.decode_address(address) == account_id


def test_derive_address1():
    # From example request and response:
    # https://xrpl.org/wallet_propose.html
    public_key = bytes.fromhex(
        '0330E7FC9D56BB25D6893BA3F317AE5BCF33B3291BD63DB32654A313222F7FD020'
    )
    address = 'rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh'
    account_id = derive_account_id(public_key)
    assert codec.encode_address(account_id) == address


def test_derive_address2():
    # From example in section "Address Encoding":
    # https://xrpl.org/accounts.html#address-encoding
    public_key = bytes.fromhex(
        'ED9434799226374926EDA3B54B1B461B4ABF7237962EAE18528FEA67595397FA32'
    )
    address = 'rDTXLQ7ZKZVKz33zJbHjgVShjsBnqMBhmN'
    account_id = derive_account_id(public_key)
    assert codec.encode_address(account_id) == address
