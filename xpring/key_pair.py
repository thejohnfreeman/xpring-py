from dataclasses import dataclass
import typing as t

from xpring.algorithms.signing import SigningAlgorithm
from xpring.codec import DEFAULT_CODEC
from xpring.hashes import ripemd160, sha256
from xpring.key import Key

Address = str


@dataclass
class KeyPair:
    public_key: Key
    private_key: Key
    algorithm: SigningAlgorithm

    @classmethod
    def from_seed(cls, seed: str) -> 'KeyPair':
        entropy, algorithm = DEFAULT_CODEC.decode_seed(seed)
        public_key, private_key = algorithm.derive_key_pair(entropy)
        # TODO: Is this assertion necessary?
        message = b'The quick brown fox jumped over the lazy dog.'
        signature = algorithm.sign(message, private_key)
        if not algorithm.verify(message, signature, public_key):
            raise AssertionError('public key does not verify private key')
        return cls(public_key, private_key, algorithm)

    @property
    def address(self) -> Address:
        address = ripemd160(sha256(self.public_key.bytes))
        return DEFAULT_CODEC.encode_address(address)

    def sign(self, message: bytes) -> bytes:
        return self.algorithm.sign(message, self.private_key)

    def verify(self, message: bytes, signature: bytes) -> bytes:
        return self.algorithm.verify(message, signature, self.public_key)
