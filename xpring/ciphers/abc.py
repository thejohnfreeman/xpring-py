from typing_extensions import Protocol


class Cipher(Protocol):
    SEED_PREFIX: bytes
