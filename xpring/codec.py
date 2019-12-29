import enum
from itertools import takewhile
import math
import typing as t

from xpring import hashes
from xpring.algorithms import ed25519, SigningAlgorithm, SIGNING_ALGORITHMS
from xpring.types import AccountId, Address, EncodedSeed, PublicKey, Seed

ADDRESS_PREFIX = b'\x00'


def ilen(iterator):
    # https://stackoverflow.com/a/3345797/618906
    # Iterators do not define `__len__`, even though they could.
    return sum(1 for _ in iterator)


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
        zeroes = ilen(takewhile(lambda b: b == 0, bites))
        i = int.from_bytes(bites[zeroes:], 'big')
        s = ''
        while i:
            i, digit = divmod(i, self.base)
            s = self.alphabet[digit] + s
        return (self.alphabet[0] * zeroes) + s

    def encode_with_checksum(self, bites: bytes) -> str:
        checksum = self.checksum(bites)
        return self.encode(bites + checksum)

    def encode_seed(
        self, seed: Seed, algorithm: SigningAlgorithm = ed25519
    ) -> str:
        if len(seed) != 16:
            raise ValueError('seed must have exactly 16 bytes of entropy')
        return self.encode_with_checksum(algorithm.SEED_PREFIX + seed)

    def encode_address(self, account_id: AccountId) -> Address:
        return t.cast(
            Address, self.encode_with_checksum(ADDRESS_PREFIX + account_id)
        )

    def decode(self, string: str) -> bytes:
        zeroes = ilen(takewhile(lambda c: c == self.alphabet[0], string))
        sigfig = string[zeroes:]
        sum = 0
        for c in sigfig:
            sum = sum * self.base + self.alphabet.index(c)
        # Special-case the first character to avoid overshooting.
        max = pow(self.base, len(sigfig) - 1) * self.alphabet.index(sigfig[0])
        # 256 is the base for byte encoding.
        length = math.ceil(math.log(max, 256))
        return (b'\0' * zeroes) + sum.to_bytes(length, 'big')

    def decode_with_checksum(self, string: str) -> bytes:
        bites = self.decode(string)
        checksum = bites[-4:]
        payload = bites[:-4]
        if self.checksum(payload) != checksum:
            raise ValueError('wrong checksum')
        return payload

    def decode_seed(
        self,
        encoded_seed: EncodedSeed,
        algorithms: t.Iterable[SigningAlgorithm] = SIGNING_ALGORITHMS
    ) -> t.Tuple[Seed, SigningAlgorithm]:
        payload = self.decode_with_checksum(encoded_seed)
        for algorithm in algorithms:
            if payload.startswith(algorithm.SEED_PREFIX):
                seed = payload[len(algorithm.SEED_PREFIX):]
                return (t.cast(Seed, seed), algorithm)
        raise ValueError('unknown signing algorithm')

    def decode_address(self, address: Address) -> AccountId:
        account_id = self.decode_with_checksum(address)
        return t.cast(AccountId, account_id[len(ADDRESS_PREFIX):])


DEFAULT_CODEC = Codec()
