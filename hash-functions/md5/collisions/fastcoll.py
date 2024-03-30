from md5 import MD5, rotl, rotr

# from os import urandom
from random import randrange
import struct

md = MD5()
init = md.init
s = md.s
f = md.f
w = md.w
t = md.t


def compress(h, block: bytes):
    state = struct.unpack("<16I", block)

    a, b, c, d = h
    qs = []

    for i in range(64):
        fi = f[i // 16](b, c, d)
        wi = w[i // 16](state, i)
        ti = t[i]
        si = s[i]

        q = (b + rotl((a + fi + wi + ti) % 2**32, si)) % 2**32  # q_i = q_{i-1} + ...
        qs.append(q)
        # if i in range(0, 32):
        #    print("No: ", w[i // 16](list(range(16)), i))

        # if i in range(32, 36):
        #    print("Should: ", w[i // 16](list(range(16)), i))

        a, b, c, d = d, q, b, c

    return [(x + y) % 2**32 for x, y in zip([a, b, c, d], h)], qs


w_inv = []
w_inv.append(lambda i: i)
w_inv.append(lambda i: (13 * (i - 1)) % 16)
w_inv.append(lambda i: (11 * (i - 5)) % 16)
w_inv.append(lambda i: 7 * i % 16)


def decompress(qs, h):  # qs from 0 to 15
    a0, b0, c0, d0 = h

    m = [0 for _ in range(16)]
    qs = {i: qs[i] for i in range(16)}
    qs[-1] = b0
    qs[-2] = c0
    qs[-3] = d0
    qs[-4] = a0

    for i in reversed(range(16)):
        fi = f[i // 16](qs[i - 1], qs[i - 2], qs[i - 3])
        ti = t[i]
        si = s[i]

        Si = rotr((qs[i] - qs[i - 1]) % 2**32, si)
        w_i = (Si - fi - ti - qs[i - 4]) % 2**32
        m[w_inv[i // 16](i)] = w_i
    return m


qs = [randrange(0, 2**32) for _ in range(16)]
m = struct.pack("<16I", *decompress(qs, init))
_, q = compress(init, m)

print(qs)
print(q[:16])
