import typing_extensions as tex

from ecdsa.curves import Curve


class HashFunction(tex.Protocol):
    ...


class SigningKey:

    @classmethod
    def from_string(
        cls, data: bytes, curve: Curve, hashfunc: HashFunction = None
    ) -> 'SigningKey':
        ...


class VerifyingKey:

    @classmethod
    def from_pem(
        cls, string: bytes, hashfunc: HashFunction = None
    ) -> 'VerifyingKey':
        ...
