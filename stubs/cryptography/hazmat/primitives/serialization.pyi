from enum import Enum

from cryptography.hazmat.backends import Backend
from cryptography.hazmat.primitives.asymmetric.ec import PublicKey


class Encoding(Enum):
    PEM = 'PEM'


class PublicFormat(Enum):
    SubjectPublicKeyInfo = "X.509 subjectPublicKeyInfo with PKCS#1"


def load_pem_public_key(data: bytes, backend: Backend) -> PublicKey:
    ...
