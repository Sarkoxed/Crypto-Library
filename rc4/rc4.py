class RC4:
    S: list[int] = []
    i: int = 0
    j: int = 0

    def __init__(self, key: bytes):
        if len(key) == 0:
            raise ValueError("invalid keylength")

        S = [i for i in range(256)]
        j = 0
        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) % 256
            S[i], S[j] = S[j], S[i]

        self.S = S
        self.i = 0
        self.j = 0

    def next(self):
        self.i = (self.i + 1) % 256
        self.j = (self.j + self.S[self.i]) % 256
        self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]
        K = self.S[(self.S[self.i] + self.S[self.j]) % 256]
        return K

    def encrypt(self, pl: bytes):
        pl = list(pl)

        for i in range(len(pl)):
            pl[i] ^= self.next()
        return bytes(pl)

if __name__ == "__main__":
    from Crypto.Cipher import ARC4
    from os import urandom
    from random import randint
    
    for i in range(1000):
        key = urandom(randint(5, 255))
        plaintext = urandom(randint(1, 1000))
    
        cip1 = ARC4.new(key)
        cip2 = RC4(key)
    
        assert cip1.encrypt(plaintext) == cip2.encrypt(plaintext)
        assert cip1.encrypt(plaintext) == cip2.encrypt(plaintext)
