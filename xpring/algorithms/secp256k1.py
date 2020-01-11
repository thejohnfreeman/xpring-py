import typing as t

from fastecdsa import curve, ecdsa, keys

from xpring import hashes
from xpring.algorithms.signing import Seed, PrivateKey, PublicKey, Signature


def to_bytes(i: int, length: int) -> bytes:
    return i.to_bytes(length, byteorder='big', signed=False)


def from_bytes(bites: bytes) -> int:
    return int.from_bytes(bites, byteorder='big', signed=False)


SEED_PREFIX = b'\x21'
FAMILY = bytes(4)

GROUP_ORDER = from_bytes(
    bytes.
    fromhex('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141')
)
assert curve.secp256k1.q == GROUP_ORDER


def derive_private_key(seed: bytes) -> int:
    sequence = 0
    while True:
        buffer = seed + to_bytes(sequence, 4)
        private_key = from_bytes(hashes.sha512half(buffer))
        if private_key != 0 and private_key < GROUP_ORDER:
            return private_key
        sequence += 1


def compress_ecdsa_point(point) -> PublicKey:
    prefix = b'\x03' if point.y % 2 else b'\x02'
    return t.cast(PublicKey, prefix + to_bytes(point.x, 32))


def derive_key_pair(seed: Seed) -> t.Tuple[PrivateKey, PublicKey]:
    root_private_key = derive_private_key(seed)
    root_public_point = keys.get_public_key(root_private_key, curve.secp256k1)
    root_public_key = compress_ecdsa_point(root_public_point)

    inter_private_key = derive_private_key(root_public_key + FAMILY)
    inter_public_point = keys.get_public_key(inter_private_key, curve.secp256k1)
    inter_public_key = compress_ecdsa_point(inter_public_point)

    master_private_key = to_bytes(
        (root_private_key + inter_private_key) % GROUP_ORDER, 32
    )
    master_public_point = root_public_point + inter_public_point
    master_public_key = compress_ecdsa_point(master_public_point)

    return (
        t.cast(PrivateKey, master_private_key),
        t.cast(PublicKey, master_public_key),
    )


def sign(message: bytes, private_key: PrivateKey) -> Signature:
    return b''


def verify(message: bytes, signature: Signature, public_key: PublicKey) -> bool:
    return True
