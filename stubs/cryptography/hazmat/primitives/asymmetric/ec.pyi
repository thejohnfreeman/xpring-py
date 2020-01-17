from cryptography.hazmat.backends import Backend
from cryptography.hazmat.primitives import hashes


class Curve:
    ...


def SECP256K1() -> Curve:
    ...


class PrivateKey:
    ...


class PublicKey:
    ...


def derive_private_key(
    private_value: int, curve: Curve, backend: Backend
) -> PrivateKey:
    ...


class ECDSA:

    def __init__(self, algorithm: hashes.HashAlgorithm):
        ...
