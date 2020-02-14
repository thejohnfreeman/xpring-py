def to_bytes(i: int, length: int) -> bytes:
    return i.to_bytes(length, byteorder='big', signed=False)


def from_bytes(bites: bytes) -> int:
    return int.from_bytes(bites, byteorder='big', signed=False)
