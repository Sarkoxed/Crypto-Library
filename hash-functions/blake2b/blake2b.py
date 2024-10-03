import struct
from decimal import Decimal, getcontext
from math import floor

getcontext().prec = 30


def rotl64(x, k):
    return ((x << k) | (x >> (64 - k))) & (2**64 - 1)


def rotr64(x, k):
    return rotl64(x, 64 - k)


# TODO: switch to iterated
def frac_sqrt(n):
    tmp = Decimal(n).sqrt()
    return tmp - floor(tmp)


class Blake2b:
    def __init__(self, digest_size: int = 64, key: bytes = None):
        # word size
        self.w = 64
        # rounds
        self.r = 12
        # rotation constants
        self.R1 = 32
        self.R2 = 24
        self.R3 = 16
        self.R4 = 63
        # block bytes
        self.bb = 128

        # hash bytes
        assert 1 <= digest_size <= 64
        self.nn = digest_size

        if key is None:
            self.kk = 0
            self.key = None
            self.tail = b""
        else:
            assert 1 <= len(key) <= 64
            self.kk = len(key)
            padlen = -len(key) % self.bb
            self.tail = key + padlen * b"\x00"

        primes = [2, 3, 5, 7, 11, 13, 17, 19]
        self.iv = [floor(2**self.w * frac_sqrt(p)) for p in primes]

        self.sigma = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            [14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3],
            [11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4],
            [7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8],
            [9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13],
            [2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9],
            [12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11],
            [13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10],
            [6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5],
            [10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0],
        ]

        self.p = [int.from_bytes(bytes([0x01, 0x01, self.kk, self.nn]), "little")] + [
            0
        ] * 7
        self.t = self.bb

        # state
        self.h = self.iv.copy()
        self.h[0] ^= 0x01010000 ^ (self.kk << 8) ^ self.nn

        self.finished = False

    def Gmix(self, v: list[int], a: int, b: int, c: int, d: int, x: int, y: int):
        v[a] = (v[a] + v[b] + x) % 2**self.w
        v[d] = rotr64(v[d] ^ v[a], self.R1)
        v[c] = (v[c] + v[d]) % 2**self.w
        v[b] = rotr64(v[b] ^ v[c], self.R2)

        v[a] = (v[a] + v[b] + y) % 2**self.w
        v[d] = rotr64(v[d] ^ v[a], self.R3)
        v[c] = (v[c] + v[d]) % 2**self.w
        v[b] = rotr64(v[b] ^ v[c], self.R4)
        return v

    def compress(self, block: list[int], is_final: bool):
        v = self.h.copy() + self.iv.copy()
        v[12] ^= self.t % 2**self.w
        v[13] ^= self.t >> self.w

        if is_final:
            v[14] ^= 2**self.w - 1

        for i in range(self.r):
            s = self.sigma[i % 10]

            v = self.Gmix(v, 0, 4, 8, 12, block[s[0]], block[s[1]])
            v = self.Gmix(v, 1, 5, 9, 13, block[s[2]], block[s[3]])
            v = self.Gmix(v, 2, 6, 10, 14, block[s[4]], block[s[5]])
            v = self.Gmix(v, 3, 7, 11, 15, block[s[6]], block[s[7]])

            v = self.Gmix(v, 0, 5, 10, 15, block[s[8]], block[s[9]])
            v = self.Gmix(v, 1, 6, 11, 12, block[s[10]], block[s[11]])
            v = self.Gmix(v, 2, 7, 8, 13, block[s[12]], block[s[13]])
            v = self.Gmix(v, 3, 4, 9, 14, block[s[14]], block[s[15]])

        for i in range(8):
            self.h[i] ^= v[i] ^ v[i + 8]

    def update(self, data: bytes, is_final: bool):
        assert not self.finished

        data = self.tail + data
        self.tail = b""

        if is_final:
            ll = self.t - self.bb + len(data)
            padlen = -len(data) % self.bb
            data += b"\x00" * padlen
        else:
            ll = 0
            taillen = len(data) % self.bb
            self.tail = data[-taillen:]
            data = data[:-taillen]

        blocks = [
            struct.unpack("<16Q", data[i : i + self.bb])
            for i in range(0, len(data), self.bb)
        ]

        for block in blocks[:-1]:
            self.compress(block, False)
            self.t += self.bb

        if not is_final:
            self.compress(blocks[-1], False)
            self.t += self.bb
        else:
            self.finished = True
            self.t = ll

            if self.kk == 0:
                self.compress(blocks[-1], True)
            else:
                self.t += self.bb
                self.compress(blocks[-1], True)

    def digest(self):
        dig = struct.pack("<8Q", *self.h)
        return dig[: self.nn]

    def hexdigest(self):
        return self.digest().hex()


if __name__ == "__main__":
    blake = Blake2b()
    blake.update(b"aboba", True)
    print(blake.hexdigest())
