import pytest

from xpring.key_pair import KeyPair
from xpring.types import (
    Address, EncodedSeed, PrivateKey, PublicKey, Signature
)


class TestCase:

    def __init__(
        self,
        encoded_seed: str,
        private_key: str,
        public_key: str,
        address: str,
        signature: str,
    ):
        self.encoded_seed = encoded_seed
        self.private_key = bytes.fromhex(private_key)
        self.public_key = bytes.fromhex(public_key)
        self.address = address
        self.signature = bytes.fromhex(signature)


# https://github.com/ripple/ripple-keypairs/blob/6f606a885ae5cb2e897c796c98171938aba19903/test/fixtures/api.json#L12-L21
TEST_CASES = (
    'test_case', (
        TestCase(
            'sEdSKaCy2JT7JaM7v95H9SxkhP9wS2r',
            'B4C4E046826BD26190D09715FC31F4E6A728204EADD112905B08B14B7F15C4F3',
            'ED01FA53FA5A7E77798F882ECE20B1ABC00BB358A9E55A202D0D0676BD0CE37A63',
            'rLUEXYuLiQptky37CqLcm9USQpPiz5rkpD',
            'CB199E1BFD4E3DAA105E4832EEDFA36413E1F44205E4EFB9E27E826044C21E3E2E848BBC8195E8959BADF887599B7310AD1B7047EF11B682E0D068F73749750E',
        ),
        TestCase(
            'sp5fghtJtpUorTwvof1NpDXAzNwf5',
            'D78B9735C3F26501C7337B8A5727FD53A6EFDBC6AA55984F098488561F985E23',
            '030D58EB48B4420B1F7B9DF55087E0E29FEF0E8468F9A6825B01CA2C361042D435',
            'rU6K7V3Po4snVhBBaU29sesqs2qTQJWDw1',
            '30440220583A91C95E54E6A651C47BEC22744E0B101E2C4060E7B08F6341657DAD9BC3EE02207D1489C7395DB0188D3A56A977ECBA54B36FA9371B40319655B1B4429E33EF2D',
        ),
    )
)

MESSAGE = b'test message'


@pytest.mark.parametrize(*TEST_CASES)
def test_private_key(test_case):
    key_pair = KeyPair.from_encoded_seed(test_case.encoded_seed)
    assert key_pair.private_key == test_case.private_key


@pytest.mark.parametrize(*TEST_CASES)
def test_public_key(test_case):
    key_pair = KeyPair.from_encoded_seed(test_case.encoded_seed)
    assert key_pair.public_key == test_case.public_key


@pytest.mark.parametrize(*TEST_CASES)
def test_address(test_case):
    key_pair = KeyPair.from_encoded_seed(test_case.encoded_seed)
    assert key_pair.address == test_case.address


@pytest.mark.skip
@pytest.mark.parametrize(*TEST_CASES)
def test_sign(test_case):
    key_pair = KeyPair.from_encoded_seed(test_case.encoded_seed)
    assert key_pair.sign(MESSAGE) == test_case.signature
