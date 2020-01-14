import hashlib

from xpring import hashes

# Example key, message, and signature (i.e. the test vector) come from here:
# https://github.com/ripple/ripple-keypairs/blob/master/test/fixtures/api.json#L2-L11
private_key_bytes = bytes.fromhex(
    'd78b9735c3f26501c7337b8a5727fd53a6efdbc6aa55984f098488561f985e23'
)
assert len(private_key_bytes) == 32
message_bytes = b'test message'
message_hash_bytes = hashes.sha512half(message_bytes)
assert message_hash_bytes.hex(
) == '950b2a7effa78f51a63515ec45e03ecebe50ef2f1c41e69629b50778f11bc080'
expected_signature_hex = '30440220583a91c95e54e6a651c47bec22744e0b101e2c4060e7b08f6341657dad9bc3ee02207d1489c7395db0188d3a56a977ecba54b36fa9371b40319655b1b4429e33ef2d'


class Sha512Half:
    digest_size = 32
    block_size = hashlib.sha512().block_size
    name = 'sha512half'

    def __init__(self, data: bytes = b'') -> None:
        self.data = bytes(data)

    def update(self, data: bytes) -> None:
        self.data += bytes(data)

    def digest(self) -> bytes:
        return hashes.sha512half(self.data)

    def hexdigest(self) -> str:
        return self.digest().hex()

    def copy(self) -> 'Sha512Half':
        return self.__class__(self.data)


class NoHash:
    digest_size = 32
    block_size = 32
    name = 'none'

    def __init__(self, data: bytes = b'') -> None:
        self.data = bytes(data)

    def update(self, data: bytes) -> None:
        self.data += bytes(data)

    def digest(self) -> bytes:
        return self.data

    def hexdigest(self) -> str:
        return self.digest().hex()

    def copy(self) -> 'NoHash':
        return self.__class__(self.data)
