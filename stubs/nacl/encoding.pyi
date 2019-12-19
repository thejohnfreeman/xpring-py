import typing as t
import typing_extensions as tex


class Encoder(tex.Protocol):

    @staticmethod
    def encode(data: bytes) -> t.Any:
        ...

    @staticmethod
    def decode(data: t.Any) -> bytes:
        ...


RawEncoder: Encoder
