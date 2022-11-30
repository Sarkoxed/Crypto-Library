from Crypto.Cipher import ARC4
from os import urandom


class OracleC:
    main_key: bytes = b"O\x89\xbd\xb1\x9de\xe6" + b'UU\xb5\xc4O\x9c\xea'

    def __init__(self, pre: bool, keylen: int = 64):
        self.IV = urandom(keylen - len(self.main_key))
        if pre:
            self.cipher = ARC4.new(self.main_key + self.IV)
        else:
            self.cipher = ARC4.new(self.IV + self.main_key)

    def call(self):
        return self.cipher.encrypt(b"\x00")[0]


class OracleO:
    S: list[int] = []
    i: int = 0
    j: int = 0
    main_key: bytes = b"crypto{some_not_random_but_cool}"
    trace: list[int] = []

    def __init__(self, pre: bool, keylen: int = 64):
        self.IV = urandom(keylen - len(self.main_key))
        if pre:
            self.key = self.main_key + self.IV
        else:
            self.key = self.IV + self.main_key

        S = [i for i in range(256)]
        j = 0
        for i in range(256):
            j = (j + S[i] + self.key[i % len(self.key)]) % 256
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

    def call(self):
        return self.encrypt(b"\x00")[0]
