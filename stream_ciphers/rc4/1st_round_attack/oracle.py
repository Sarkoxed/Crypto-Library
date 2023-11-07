from Crypto.Cipher import ARC4
from os import urandom
from typing import Optional


class OracleC:
    main_key: bytes = b""

    def __init__(
        self,
        pre: bool,
        keylen: int = 64,
        main_key: bytes = b"crypto{some_not_random_but_cool}",
        IV: Optional[bytes] = None
    ):
        self.main_key = main_key
        if IV is None:
            self.IV = urandom(keylen - len(self.main_key))
        else:
            self.IV = IV

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
    main_key: bytes = b""
    trace: list[int] = []  # debug

    def __init__(
        self,
        pre: bool,
        n: int = 256,
        keylen: int = 64,
        main_key: bytes = b"crypto{some_not_random_but_cool}",
        IV: Optional[bytes] = None
    ):
        self.n = n
        self.main_key = main_key
        if IV is None:
            self.IV = urandom(keylen - len(self.main_key))
        else:
            self.IV = IV

        if pre:
            self.key = self.main_key + self.IV
        else:
            self.key = self.IV + self.main_key

        S = [i for i in range(self.n)]
        j = 0
        for i in range(self.n):
            j = (j + S[i] + self.key[i % len(self.key)]) % self.n
            S[i], S[j] = S[j], S[i]

        self.S = S
        self.i = 0
        self.j = 0

    def next(self):
        self.i = (self.i + 1) % self.n
        self.j = (self.j + self.S[self.i]) % self.n
        self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]
        K = self.S[(self.S[self.i] + self.S[self.j]) % self.n]
        return K

    def encrypt(self, pl: list[int]):
        for i in range(len(pl)):
            pl[i] ^= self.next()
        return bytes(pl)

    def call(self):
        return self.encrypt([0])[0]
