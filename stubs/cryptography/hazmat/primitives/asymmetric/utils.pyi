from cryptography.hazmat.primitives import hashes


class Prehashed(hashes.HashAlgorithm):

    def __init__(self, algorithm: hashes.HashAlgorithm):
        self.digest_size = algorithm.digest_size
