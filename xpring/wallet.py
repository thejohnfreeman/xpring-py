import typing as t

from xpring.hashes import sha512half
from xpring.key_pair import KeyPair
from xpring.serialization import PREFIX_TRANSACTION_ID, serialize_transaction
from xpring.types import (
    AccountId,
    Address,
    EncodedSeed,
    Seed,
    PrivateKey,
    PublicKey,
    Signature,
    SignedTransaction,
    Transaction,
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

    def sign(self, message: bytes) -> Signature:
        return self.key_pair.sign(message)

    def sign_transaction(self, transaction: Transaction) -> SignedTransaction:
        blob = serialize_transaction(transaction, signing=True)
        signature = self.sign(blob)
        digest = sha512half(PREFIX_TRANSACTION_ID + blob)
        return {
            **transaction,
            'SigningPubKey': self.public_key.hex().upper(),
            'TxnSignature': signature.hex().upper(),
            'hash': digest.hex().upper(),
        }

    def verify(self, message: bytes, signature: bytes) -> bool:
        return self.key_pair.verify(message, t.cast(Signature, signature))
