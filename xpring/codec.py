import enum
import math
import typing as t

from xpring import hashes
from xpring.algorithms import ed25519, SigningAlgorithm, SIGNING_ALGORITHMS
from xpring.types import AccountId, Address, EncodedSeed, PublicKey, Seed

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
        zeroes = len(bites)
        sigfig = bites.lstrip(b'\0')
        zeroes -= len(sigfig)
        i = int.from_bytes(sigfig, 'big')
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
        zeroes = len(string)
        sigfig = string.lstrip(self.alphabet[0])
        zeroes -= len(sigfig)
        number = 0
        for c in sigfig:
            number = number * self.base + self.alphabet.index(c)
        # How many bytes do we need to represent this integer?
        length = math.ceil(math.log(number, 256))
        return (b'\0' * zeroes) + number.to_bytes(length, 'big')

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
