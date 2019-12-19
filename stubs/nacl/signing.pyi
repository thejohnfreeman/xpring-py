from nacl.encoding import Encoder, RawEncoder


class SigningKey:

    def __init__(self, seed: bytes, encoder: Encoder = RawEncoder) -> None:
        ...

    verify_key: VerifyKey

    def sign(
        self, message: bytes, encoder: Encoder = RawEncoder
    ) -> SignedMessage:
        ...


class VerifyKey:

    def __init__(self, key: bytes, encoder: Encoder = RawEncoder) -> None:
        ...

    _key: bytes

    def verify(
        self, smessage: bytes, signature: bytes, encoder: Encoder = RawEncoder
    ) -> bytes:
        ...


class SignedMessage:
    signature: bytes
    message: bytes
