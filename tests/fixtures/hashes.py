import hashlib

from xpring import hashes


class Sha512Half:
    digest_size = 32
    block_size = hashlib.sha512().block_size
    name = 'sha512half'

    def __init__(self, data: bytes = b'') -> None:
        self.data = bytes(data)

    def update(self, data: bytes) -> None:
        self.data += bytes(data)

    def digest(self) -> bytes:
        return hashes.sha512half(self.data)

    def hexdigest(self) -> str:
        return self.digest().hex()

    def copy(self) -> 'Sha512Half':
        return self.__class__(self.data)
