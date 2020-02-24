import typing_extensions as tex

from ecdsa.curves import Curve
from ecdsa.util import Decoder, Encoder, sigencode_string


class HashFunction(tex.Protocol):
    ...


class SigningKey:

    verifying_key: VerifyingKey

    @classmethod
    def from_string(
        cls, data: bytes, curve: Curve, hashfunc: HashFunction = None
    ) -> 'SigningKey':
        ...

    def sign_deterministic(
        self,
        data: bytes,
        hashfunc: HashFunction = None,
        sigencode: Encoder = sigencode_string,
    ) -> bytes:
        ...

    def sign_digest_deterministic(
        self,
        digest: bytes,
        hashfunc: HashFunction = None,
        sigencode: Encoder = sigencode_string,
    ) -> bytes:
        ...


class VerifyingKey:

    @classmethod
    def from_string(cls, string: bytes, curve: Curve) -> 'VerifyingKey':
        ...

    @classmethod
    def from_pem(
        cls, string: bytes, hashfunc: HashFunction = None
    ) -> 'VerifyingKey':
        ...

    def verify(
        self,
        signature: bytes,
        message: bytes,
        hashfunc: HashFunction,
        sigdecode: Decoder,
    ) -> bool:
        ...

    def to_pem(self) -> bytes:
        ...
