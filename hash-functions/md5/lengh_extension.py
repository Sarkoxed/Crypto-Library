from md5 import MD5
import struct


def pad(m):
    mes_lengh = len(m)
    m += b"\x80"
    m += b"\x00" * ((56 - (mes_lengh + 1) % 64) % 64)

    message_bit_length = mes_lengh * 8
    m += struct.pack(b"<Q", message_bit_length)
    print(m)
    return m


def length_extension_attack(prev_hash: bytes, known_length: int, tail: bytes):
    s = MD5()
    h = struct.unpack("<4I", prev_hash)
    init = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]
    A, B, C, D = [(x - y) % 2**32 for x, y in zip(h, init)]

    s.h[0] = A
    s.h[-1] = B
    s.h[-2] = C
    s.h[-3] = D

    s.length = known_length
    s.update(tail)
    return s.digest()


if __name__ == "__main__":
    secret = b"random"
    message = b"kek"
    tail = b"aboba"

    h1 = MD5()
    h1.update(secret + message)
    h1 = h1.digest()

    tmp = b"\x00" * len(secret) + message
    res1 = length_extension_attack(h1, len(pad(tmp)) * 8, tail)

    padded = pad(secret + message)
    res2 = MD5()
    res2.update(padded + tail)
    res2 = res2.digest()

    print(res1 == res2)
