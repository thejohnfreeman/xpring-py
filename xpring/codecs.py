import enum

import baseconv
import nacl.encoding
import nacl.hash


def sha256(message: bytes) -> bytes:
    return nacl.hash.sha256(message, encoder=nacl.encoding.RawEncoder())


def checksum(message: bytes) -> bytes:
    return sha256(sha256(message))[:4]


class Encoding(enum.Enum):
    ED25519 = b'\x01\xE1\x4B'
    SECP256K1 = b'\x21'


class Codec:

    def __init__(
        self,
        alphabet='rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz',
        checksum=checksum
    ):
        self.alphabet = alphabet
        self.codec = baseconv.BaseConverter(alphabet)
        self.base = len(alphabet)
        self.checksum = checksum

    def encode(self, message: bytes) -> bytes:
        check = self.checksum(message)
        return self.codec.encode(int.from_bytes(message + check, 'big'))

    def encode_seed(
        self, seed: str, encoding: Encoding = Encoding.ED25519
    ) -> bytes:
        message = encoding.value + bytes.fromhex(seed)
        return self.encode(message)
