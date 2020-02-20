from dataclasses import dataclass
import typing as t

from xpring import hashes
from xpring.types import (
    AccountId, Address, EncodedSeed, Seed, PrivateKey, PublicKey, Signature
)
from xpring.algorithms.signing import SigningAlgorithm
from xpring.codec import DEFAULT_CODEC


def derive_account_id(public_key: PublicKey) -> AccountId:
    # https://xrpl.org/accounts.html#address-encoding
    account_id = hashes.ripemd160(hashes.sha256(public_key))
    return t.cast(AccountId, account_id)


@dataclass
class KeyPair:
    seed: Seed
    algorithm: SigningAlgorithm
    private_key: PrivateKey
    public_key: PublicKey

    @classmethod
    def from_encoded_seed(cls, encoded_seed: EncodedSeed) -> 'KeyPair':
        seed, algorithm = DEFAULT_CODEC.decode_seed(encoded_seed)
        private_key, public_key = algorithm.derive_key_pair(seed)
        # TODO: Is this assertion necessary?
        message = b'The quick brown fox jumped over the lazy dog.'
        signature = algorithm.sign(message, private_key)
        if not algorithm.verify(message, signature, public_key):
            raise AssertionError('public key does not verify private key')
        return cls(seed, algorithm, private_key, public_key)

    @property
    def account_id(self) -> AccountId:
        # TODO: cached_property?
        return derive_account_id(self.public_key)

    @property
    def address(self) -> Address:
        return DEFAULT_CODEC.encode_address(self.account_id)

    def sign(self, message: bytes) -> Signature:
        return self.algorithm.sign(message, self.private_key)

    def verify(self, message: bytes, signature: Signature) -> bool:
        return self.algorithm.verify(message, signature, self.public_key)
