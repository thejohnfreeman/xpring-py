from dataclasses import dataclass
import typing as t

from xpring import ciphers, codecs, hashes


@dataclass
class KeyPair:
    public_key: t.Any
    private_key: t.Any
    cipher: ciphers.Cipher

    def sign(self, message: bytes) -> bytes:
        return self.cipher.sign(message, self.private_key)

    def verify(self, message: bytes, signature: bytes) -> bool:
        return self.cipher.verify(message, signature, self.public_key)


def derive_key_pair(seed: str):
    entropy, cipher = codecs.DEFAULT_CODEC.decode_seed(seed)
    public_key, private_key = cipher.derive_key_pair(entropy)
    # TODO: Is this assertion necessary?
    message = b'The quick brown fox jumped over the lazy dog.'
    signature = cipher.sign(message, private_key)
    if not cipher.verify(message, signature, public_key):
        raise AssertionError('public key does not verify private key')
    return KeyPair(public_key, private_key, cipher)
