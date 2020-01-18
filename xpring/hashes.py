import hashlib

import nacl.encoding
import nacl.hash


def sha256(bites: bytes) -> bytes:
    return nacl.hash.sha256(bites, encoder=nacl.encoding.RawEncoder)


def checksum(bites: bytes) -> bytes:
    return sha256(sha256(bites))[:4]


def sha512half(bites: bytes) -> bytes:
    return nacl.hash.sha512(bites, encoder=nacl.encoding.RawEncoder)[:32]


def ripemd160(bites: bytes) -> bytes:
    hasher = hashlib.new('ripemd160')
    hasher.update(bites)
    return hasher.digest()


class IdentityHash:
    digest_size = 32
    block_size = 32
    name = 'identity'

    def __init__(self, data: bytes = b'') -> None:
        self.data = bytes(data)

    def update(self, data: bytes) -> None:
        self.data += bytes(data)

    def digest(self) -> bytes:
        return self.data

    def hexdigest(self) -> str:
        return self.digest().hex()

    def copy(self) -> 'IdentityHash':
        return self.__class__(self.data)
