from xpring.key_pairs import KeyPair


class Wallet:

    def __init__(self, key_pair: KeyPair):
        self.key_pair = key_pair

    @classmethod
    def from_seed(cls, seed):
        key_pair = KeyPair.from_seed(seed)
        return cls(key_pair)

    @property
    def address(self):
        return self.key_pair.address

    @property
    def public_key(self):
        return self.key_pair.public_key

    @property
    def private_key(self):
        return self.key_pair.private_key

    def sign(self, message: bytes) -> bytes:
        return self.key_pair.sign(message)

    def verify(self, message: bytes, signature: bytes) -> bool:
        return self.key_pair.verify(message, signature)
