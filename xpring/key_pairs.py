from xpring import codecs, hashes


def derive_key_pair(seed: str):
    entropy, cipher = codecs.DEFAULT_CODEC.decode_seed(seed)
    public_key, private_key = cipher.derive_key_pair(entropy)
    # TODO: Is this assertion necessary?
    message = b'The quick brown fox jumped over the lazy dog.'
    signature = cipher.sign(message, private_key)
    if not cipher.verify(message, signature, public_key):
        raise AssertionError('public key does not verify private key')
    return (public_key, private_key)
