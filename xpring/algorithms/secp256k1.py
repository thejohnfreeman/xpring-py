import typing as t

from fastecdsa import curve, ecdsa, keys
from fastecdsa.encoding.der import DEREncoder
# We use ecdsa only for verifying, until we can decode DER with fastecdsa:
# https://github.com/AntonKueltz/fastecdsa/issues/47
from ecdsa import curves, VerifyingKey
from ecdsa.util import sigdecode_der

from xpring import hashes
from xpring.algorithms.signing import Seed, PrivateKey, PublicKey, Signature
from xpring.bits import from_bytes, to_bytes

SEED_PREFIX = b'\x21'
FAMILY = bytes(4)

GROUP_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
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
    digest = hashes.sha512half(message)
    signing_key = int.from_bytes(private_key, byteorder='big')
    r, s = ecdsa.sign(
        digest,
        signing_key,
        curve=curve.secp256k1,
        prehashed=True,
    )
    # Both (r, s) and (r, -s mod G = G - s) are valid, canonical signatures.
    # (r, s) is fully canonical only when s <= G - s.
    s_inverse = GROUP_ORDER - s
    if s > s_inverse:
        s = s_inverse
    signature = DEREncoder.encode_signature(r, s)
    return t.cast(Signature, signature)


def verify(message: bytes, signature: Signature, public_key: PublicKey) -> bool:
    digest = hashes.sha512half(message)
    # We need `ecdsa` to decompress the public key.
    # Would be nice if fastecdsa could do this.
    # TODO: Implement it ourselves.
    # https://github.com/AntonKueltz/fastecdsa/issues/47
    verifying_key = VerifyingKey.from_string(public_key, curves.SECP256k1)
    return verifying_key.verify(
        signature,
        digest,
        hashfunc=hashes.IdentityHash,
        sigdecode=sigdecode_der,
    )
