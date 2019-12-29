import typing as t
import typing_extensions as tex

from xpring.types import Seed, PrivateKey, PublicKey, Signature


class SigningAlgorithm(tex.Protocol):
    """
    Once ed25519 was added, the team wanted a way to differentiate seeds
    used with different signing algorithms. The seeds for both secp256k1 and
    ed25519 are arrays of 16 bytes, and thus could be encoded exactly the same
    way. It was decided to use a different prefix for ed25519, which yields
    encodings that always start with "sEd".
    """
    SEED_PREFIX: bytes

    def derive_key_pair(self, seed: Seed) -> t.Tuple[PrivateKey, PublicKey]:
        ...

    def sign(self, message: bytes, private_key: PrivateKey) -> Signature:
        ...

    def verify(
        self, message: bytes, signature: Signature, public_key: PublicKey
    ) -> bool:
        ...
