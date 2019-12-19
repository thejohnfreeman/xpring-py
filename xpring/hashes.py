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
