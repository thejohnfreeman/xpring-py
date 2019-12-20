import typing as t


class Key:

    def __init__(self, bites: bytes, prefix: str) -> None:
        self.bytes = bites
        self.prefix = prefix

    def __str__(self) -> str:
        return self.prefix + self.bytes.hex().upper()


KeyPair = t.Tuple[Key, Key]
