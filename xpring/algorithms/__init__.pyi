import typing as t

from xpring.algorithms.signing import SigningAlgorithm as SigningAlgorithm

ed25519: SigningAlgorithm
secp256k1: SigningAlgorithm
SIGNING_ALGORITHMS: t.Iterable[SigningAlgorithm]
