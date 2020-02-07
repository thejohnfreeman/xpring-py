import typing as t

from xpring.key_pair import KeyPair
from xpring.types import (
    AccountId, Address, EncodedSeed, Seed, PrivateKey, PublicKey, Signature
)


class Wallet:

    def __init__(self, key_pair: KeyPair):
        self.key_pair = key_pair

    @classmethod
    def from_seed(cls, seed: EncodedSeed):
        key_pair = KeyPair.from_encoded_seed(seed)
        return cls(key_pair)

    @property
    def account_id(self) -> AccountId:
        return self.key_pair.account_id

    @property
    def address(self) -> Address:
        return self.key_pair.address

    @property
    def public_key(self) -> PublicKey:
        return self.key_pair.public_key

    @property
    def private_key(self) -> PrivateKey:
        return self.key_pair.private_key

    def sign(self, message: bytes) -> bytes:
        return self.key_pair.sign(message)

    def verify(self, message: bytes, signature: bytes) -> bool:
        return self.key_pair.verify(message, t.cast(Signature, signature))
