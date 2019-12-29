from xpring.key_pair import KeyPair
from xpring.types import (
    Address, EncodedSeed, Seed, PrivateKey, PublicKey, Signature
)


class Wallet:

    def __init__(self, key_pair: KeyPair):
        self.key_pair = key_pair

    @classmethod
    def from_seed(cls, encoded_seed: EncodedSeed):
        key_pair = KeyPair.from_encoded_seed(encoded_seed)
        return cls(key_pair)

    @property
    def address(self) -> Address:
        return self.key_pair.address

    @property
    def public_key(self) -> PublicKey:
        return self.key_pair.public_key

    @property
    def private_key(self) -> PrivateKey:
        return self.key_pair.private_key
