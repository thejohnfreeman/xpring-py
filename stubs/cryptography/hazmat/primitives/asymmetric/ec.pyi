from cryptography.hazmat.backends import Backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat


class Curve:
    ...


def SECP256K1() -> Curve:
    ...


class EllipticCurveSignatureAlgorithm:
    ...


class ECDSA(EllipticCurveSignatureAlgorithm):

    def __init__(self, algorithm: hashes.HashAlgorithm):
        ...


class EllipticCurvePrivateNumbers:

    _private_value: int


class EllipticCurvePrivateKey:

    def private_numbers(self) -> EllipticCurvePrivateNumbers:
        ...

    def public_key(self) -> EllipticCurvePublicKey:
        ...

    def sign(
        self,
        data: bytes,
        signature_algorithm: EllipticCurveSignatureAlgorithm,
    ):
        ...


class EllipticCurvePublicKey:

    def public_bytes(self, encoding: Encoding, format: PublicFormat) -> bytes:
        ...

    def verify(
        self,
        signature: bytes,
        data: bytes,
        signature_algorithm: EllipticCurveSignatureAlgorithm,
    ):
        ...


def derive_private_key(
    private_value: int, curve: Curve, backend: Backend
) -> EllipticCurvePrivateKey:
    ...
