class StreamCrypter:
    def __init__(self, algorithm):
        self.rng = algorithm

    def encrypt(self, msg):
        return [(c + self.rng.next()) % 256 for c in msg]

    def decrypt(self, msg):
        return [(c - self.rng.next()) % 256 for c in msg]

    def to_bytes(self, msg):
        return [ord(c) for c in msg]

    def to_string(self, msg):
        return "".join([chr(c) for c in msg])