import typing_extensions as tex


class HashAlgorithm(tex.Protocol):

    digest_size: int

    def __init__(self, data: bytes):
        ...

    def update(self, data: bytes):
        ...

    def digest(self) -> bytes:
        ...

    def hexdigest(self) -> str:
        ...

    def copy(self) -> 'HashAlgorithm':
        ...
