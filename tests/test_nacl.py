import hashlib

from xpring import hashes


def test_sha512half():
    """Just a sanity check that we get the same result."""
    message = b'test message'
    stdlib = hashlib.sha512(message).digest()[:32]
    nacl = hashes.sha512half(message)
    assert stdlib == nacl
