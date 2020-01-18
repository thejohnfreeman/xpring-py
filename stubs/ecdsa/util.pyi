import typing as t

Decoder = t.Callable[[str, int], bytes]


def sigdecode_der(signature: str, order: int) -> bytes:
    ...


def sigencode_der_canonize(r: int, s: int, order: int):
    ...
