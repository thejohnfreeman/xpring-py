import enum
import math
import typing as t

from xpring import hashes
from xpring.ciphers import Cipher, ed25519, KNOWN_CIPHERS

SEED_PREFIX = b'\x21'
ADDRESS_PREFIX = b'\x00'


class Codec:

    def __init__(
        self,
        alphabet='rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz',
        checksum=hashes.checksum
    ):
        self.alphabet = alphabet
        self.base = len(alphabet)
        self.checksum = checksum

    def encode(self, bites: bytes) -> str:
        i = int.from_bytes(bites, 'big')
        s = ''
        while (i > 0):
            i, digit = divmod(i, self.base)
            s += self.alphabet[digit]
        return s[::-1]

    def encode_with_checksum(self, bites: bytes) -> str:
        check = self.checksum(bites)
        return self.encode(bites + check)

    def encode_seed(self, seed: bytes, cipher: Cipher = ed25519) -> str:
        if len(seed) != 16:
            raise ValueError('seed must have exactly 16 bytes of entropy')
        return self.encode_with_checksum(cipher.SEED_PREFIX + seed)

    def encode_address(self, address: bytes) -> str:
        return 'r' + self.encode_with_checksum(ADDRESS_PREFIX + address)

    def decode(self, encoded: str) -> bytes:
        i = 0
        for c in encoded:
            i = i * self.base + self.alphabet.index(c)
        # Special-case the first character to avoid overshooting.
        max = pow(self.base, len(encoded) - 1) * self.alphabet.index(encoded[0])
        # 256 is the base for byte encoding.
        length = math.ceil(math.log(max, 256))
        return i.to_bytes(length, 'big')

    def decode_with_checksum(self, encoded: str) -> bytes:
        decoded = self.decode(encoded)
        check = decoded[-4:]
        bites = decoded[:-4]
        if self.checksum(bites) != check:
            raise ValueError('wrong checksum')
        return bites

    def decode_seed(
        self, encoded: str, known_ciphers: t.Iterable[Cipher] = KNOWN_CIPHERS
    ) -> t.Tuple[bytes, Cipher]:
        bites = self.decode_with_checksum(encoded)
        for cipher in known_ciphers:
            if bites.startswith(cipher.SEED_PREFIX):
                return (bites[len(cipher.SEED_PREFIX):], cipher)
        raise ValueError('unknown encoding')

    def decode_address(self, encoded: str) -> bytes:
        bites = self.decode_with_checksum(encoded)
        return bites[len(ADDRESS_PREFIX):]


DEFAULT_CODEC = Codec()
