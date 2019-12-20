import enum
import math
import typing as t

from xpring import hashes
from xpring.algorithms import ed25519, SigningAlgorithm, SIGNING_ALGORITHMS

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

    def encode_seed(
        self, seed: bytes, algorithm: SigningAlgorithm = ed25519
    ) -> str:
        if len(seed) != 16:
            raise ValueError('seed must have exactly 16 bytes of entropy')
        # Once ed25519 was added, the team wanted a way to differentiate seeds
        # used with different signing algorithms. The seeds for both
        # secp256k1 and ed25519 are arrays of 16 bytes, and thus could be
        # encoded exactly the same way. It was decided to use a different
        # prefix for ed25519, which yields encodings that always start with
        # "sEd".
        return self.encode_with_checksum(algorithm.SEED_PREFIX + seed)

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
        self,
        encoded: str,
        algorithms: t.Iterable[SigningAlgorithm] = SIGNING_ALGORITHMS
    ) -> t.Tuple[bytes, SigningAlgorithm]:
        bites = self.decode_with_checksum(encoded)
        for algorithm in algorithms:
            if bites.startswith(algorithm.SEED_PREFIX):
                return (bites[len(algorithm.SEED_PREFIX):], algorithm)
        raise ValueError('unknown encoding')

    def decode_address(self, encoded: str) -> bytes:
        bites = self.decode_with_checksum(encoded)
        return bites[len(ADDRESS_PREFIX):]


DEFAULT_CODEC = Codec()
