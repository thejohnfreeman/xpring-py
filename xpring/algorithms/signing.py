import typing_extensions as tex

import xpring.key as xk


class SigningAlgorithm(tex.Protocol):
    SEED_PREFIX: bytes

    def derive_key_pair(self, seed: bytes) -> xk.KeyPair:
        ...

    def sign(self, message: bytes, private_key: xk.Key) -> bytes:
        ...

    def verify(
        self, smessage: bytes, signature: bytes, public_key: xk.Key
    ) -> bytes:
        ...
