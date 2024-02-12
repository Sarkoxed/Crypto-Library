# https://datatracker.ietf.org/doc/html/rfc7539

from typing import Optional
from os import urandom
import struct


class ChaCha20:
    num_rounds: int = 20

    def __init__(
        self, key: bytes, nonce: Optional[bytes] = None, counter: Optional[int] = 0
    ):
        if nonce is None:
            nonce = urandom(12)

        if len(key) != 32:
            raise ValueError(f"Keylength {len(key)} != 32")
        if len(nonce) != 12:
            raise ValueError(f"Noncelength {len(nonce)} != 12")

        self.nonce = nonce
        self.counter = counter

        self.state = []

        self.state.extend(list(struct.unpack("<4I", b"expand 32-byte k")))
        self.state.extend(list(struct.unpack("<8I", key)))

    @staticmethod
    def ror(a, n):
        return (a >> n) | (a << (32 - n) & (2**32 - 1))

    @staticmethod
    def rol(a, n):
        return ((a << n) & (2**32 - 1)) | (a >> (32 - n))

    @staticmethod
    def quarter_round(a, b, c, d):
        a = (a + b) % 2**32
        d = ChaCha20.rol(a ^ d, 16)

        c = (c + d) % 2**32
        b = ChaCha20.rol(b ^ c, 12)

        a = (a + b) % 2**32
        d = ChaCha20.rol(d ^ a, 8)

        c = (c + d) % 2**32
        b = ChaCha20.rol(b ^ c, 7)
        return a, b, c, d

    @staticmethod
    def inner_block(state):
        inds = [[0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15]]

        for i in range(4):
            (
                state[inds[i][0]],
                state[inds[i][1]],
                state[inds[i][2]],
                state[inds[i][3]],
            ) = ChaCha20.quarter_round(
                state[inds[i][0]],
                state[inds[i][1]],
                state[inds[i][2]],
                state[inds[i][3]],
            )

        for i in range(4):
            (
                state[inds[i][0]],
                state[inds[(i + 1) % 4][1]],
                state[inds[(i + 2) % 4][2]],
                state[inds[(i + 3) % 4][3]],
            ) = ChaCha20.quarter_round(
                state[inds[i][0]],
                state[inds[(i + 1) % 4][1]],
                state[inds[(i + 2) % 4][2]],
                state[inds[(i + 3) % 4][3]],
            )

    def block(self):
        curstate = self.state.copy()
        counter = (self.counter).to_bytes(4, "little")
        self.counter += 1
        curstate.extend(list(struct.unpack("<IIII", counter + self.nonce)))

        fin = curstate.copy()
        for r in range(self.num_rounds // 2):
            ChaCha20.inner_block(curstate)
        curstate = [(x + y) % 2**32 for x, y in zip(curstate, fin)]
        return curstate

    @staticmethod
    def serialize(state):
        return struct.pack("<16I", *state)

    def encrypt(self, message: bytes):
        keystream = b""
        blocknum = (len(message) + 63) // 64
        for _ in range(blocknum):
            keystream += ChaCha20.serialize(self.block())
        return bytes(x ^ y for x, y in zip(message, keystream))
