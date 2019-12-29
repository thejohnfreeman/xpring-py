import typing as t

import nacl.encoding
import nacl.signing

from xpring import hashes
from xpring.algorithms.signing import Seed, PrivateKey, PublicKey, Signature

SEED_PREFIX = b'\x01\xE1\x4B'

KEY_PREFIX = 'ED'


# https://xrpl.org/cryptographic-keys.html#ed25519-key-derivation
def derive_key_pair(seed: Seed) -> t.Tuple[PrivateKey, PublicKey]:
    private_key = hashes.sha512half(seed)
    public_key = nacl.signing.SigningKey(private_key).verify_key._key[:32]  # pylint: disable=protected-access
    return (t.cast(PrivateKey, private_key), t.cast(PublicKey, public_key))


def sign(message: bytes, private_key: PrivateKey) -> Signature:
    key = nacl.signing.SigningKey(private_key)
    signature = key.sign(message, nacl.encoding.RawEncoder).signature
    return t.cast(Signature, signature)


def verify(message: bytes, signature: Signature, public_key: PublicKey) -> bool:
    key = nacl.signing.VerifyKey(public_key)
    return key.verify(message, signature, nacl.encoding.RawEncoder) == message
