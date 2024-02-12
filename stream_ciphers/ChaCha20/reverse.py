def ror(a, n):
    return (a >> n) | (a << (32 - n) & (2**32 - 1))


def rol(a, n):
    return ((a << n) & (2**32 - 1)) | (a >> (32 - n))


def quarter_round(a, b, c, d):
    a = (a + b) % 2**32
    d = rol(a ^ d, 16)

    c = (c + d) % 2**32
    b = rol(b ^ c, 12)

    a = (a + b) % 2**32
    d = rol(d ^ a, 8)

    c = (c + d) % 2**32
    b = rol(b ^ c, 7)
    return a, b, c, d


def reverse_quarter_round(a, b, c, d):
    b = ror(b, 7) ^ c
    c = (c - d) % 2**32

    d = ror(d, 8) ^ a
    a = (a - b) % 2**32

    b = ror(b, 12) ^ c
    c = (c - d) % 2**32

    d = ror(d, 16) ^ a
    a = (a - b) % 2**32
    return a, b, c, d
