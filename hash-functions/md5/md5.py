import struct
from math import sin, floor

rotl = lambda x, k: ((x << k) | (x >> (32 - k))) & (2**32 - 1)
rotr = lambda x, k: rotl(x, 32 - k)


class MD5:
    def __init__(self):
        self.init = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]
        self.h = self.init.copy()
        self.s = (
            [7, 12, 17, 22] * 4
            + [5, 9, 14, 20] * 4
            + [4, 11, 16, 23] * 4
            + [6, 10, 15, 21] * 4
        )

        self.f = []
        self.f.append(lambda B, C, D: (B & C) | (~B & D))
        self.f.append(lambda B, C, D: (B & D) | (~D & C))
        self.f.append(lambda B, C, D: B ^ C ^ D)
        self.f.append(lambda B, C, D: C ^ (B | ~D))

        self.w = []
        self.w.append(lambda state, i: state[i])
        self.w.append(lambda state, i: state[(5 * i + 1) % 16])
        self.w.append(lambda state, i: state[(3 * i + 5) % 16])
        self.w.append(lambda state, i: state[7 * i % 16])

        print([i for i in range(16)])
        print([(5 * i + 1) % 16 for i in range(16, 32)])
        print([(3 * i + 5) % 16 for i in range(32, 48)])
        print([7 * i % 16 for i in range(48, 64)])

        self.t = [floor(2**32 * abs(sin(i))) for i in range(1, 65)]


        self.tail = b""
        self.length = 0

    def update(self, m: bytes):
        curtail = self.tail + m

        while len(curtail) >= 64:
            block = curtail[:64]
            self.length += 512
            self.compress(block)
            curtail = curtail[64:]
        self.tail = curtail

    def compress(self, block: bytes):
        state = struct.unpack("<" + "I" * 16, block)

        a, b, c, d = self.h
        qstate = [a, d, c, b]
    
        # r1
        for i in range(64):
            B, C, D = qstate[-1], qstate[-2], qstate[-3]
            fi = self.f[i // 16](B, C, D)
            wi = self.w[i // 16](state, i)
            ti = self.t[i]
            si = self.s[i]
            q = B + rotl((qstate[-4] + fi + wi + ti) % 2**32, si)
            qstate.append(q % 2**32)
            qstate = qstate[1:]

        self.h = qstate

    def digest(self):
        block = self.tail
        self.length += len(block) * 8
        block += b"\x80"
        while len(block) % 64 != 56:
            block += b"\x00"

        block += struct.pack(b"<Q", self.length)
        self.compress(block)
        
        A, B, C, D = self.h[0], self.h[-1], self.h[-2], self.h[-3]
        res = [(x + y) % 2**32 for x, y in zip(self.init, [A, B, C, D])]

        return struct.pack("<IIII", *res)

    def hexdigest(self):
        return self.digest().hex()

if __name__ == "__main__":
    md5 = MD5()
    md5.update(input().encode())
    print(md5.hexdigest())