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
        keystream = b''
        blocknum = (len(message) + 63) // 64
        for _ in range(blocknum):
            keystream += ChaCha20.serialize(self.block())
        return bytes(x ^ y for x, y in zip(message, keystream))


def test_vectors_qr():
    a = 0x11111111
    b = 0x01020304
    c = 0x9B8D6F43
    d = 0x01234567

    a, b, c, d = ChaCha20.quarter_round(a, b, c, d)
    assert a == 0xEA2A92F4
    assert b == 0xCB1CF8CE
    assert c == 0x4581472E
    assert d == 0x5881C4BB


def test_vectors_init():
    key = bytes(range(32))
    nonce = b"\x00\x00\x00\x09\x00\x00\x00\x4a\x00\x00\x00\x00"

    cipher = ChaCha20(key, nonce, counter=1)

    test_state = [
        0xE4E7F110,
        0x15593BD1,
        0x1FDD0F50,
        0xC47120A3,
        0xC7F4D1C7,
        0x368C033,
        0x9AAA2204,
        0x4E6CD4C3,
        0x466482D2,
        0x9AA9F07,
        0x5D7C214,
        0xA2028BD9,
        0xD19C12B5,
        0xB94E16DE,
        0xE883D0CB,
        0x4E3C50A2,
    ]
    
    assert cipher.block() == test_state

def test(n=1000):
    from random import randint
    from Crypto.Cipher import ChaCha20 as chch20

    for i in range(n):
        key = urandom(32)
        nonce = urandom(12)
        c1 = ChaCha20(key, nonce)
        c2 = chch20.new(key=key, nonce=nonce)
        r = b'\x00' * i

        r1 = c1.encrypt(r)
        r2 = c2.encrypt(r)
        assert r1 == r2

if __name__ == "__main__":
    test_vectors_qr()
    test_vectors_init()
    test_vectors_encrypt()
    test()
