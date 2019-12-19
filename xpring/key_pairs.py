from dataclasses import dataclass
import typing as t

from xpring import codecs, hashes
from xpring.ciphers.abc import Cipher
from xpring.key import Key

Address = str


@dataclass
class KeyPair:
    public_key: Key
    private_key: Key
    cipher: Cipher

    @classmethod
    def from_seed(cls, seed: str) -> 'KeyPair':
        entropy, cipher = codecs.DEFAULT_CODEC.decode_seed(seed)
        public_key, private_key = cipher.derive_key_pair(entropy)
        # TODO: Is this assertion necessary?
        message = b'The quick brown fox jumped over the lazy dog.'
        signature = cipher.sign(message, private_key)
        if not cipher.verify(message, signature, public_key):
            raise AssertionError('public key does not verify private key')
        return cls(public_key, private_key, cipher)

    @property
    def address(self) -> Address:
        address = hashes.ripemd160(hashes.sha256(self.public_key.bytes))
        return codecs.DEFAULT_CODEC.encode_address(address)

    def sign(self, message: bytes) -> bytes:
        return self.cipher.sign(message, self.private_key)

    def verify(self, message: bytes, signature: bytes) -> bytes:
        return self.cipher.verify(message, signature, self.public_key)
