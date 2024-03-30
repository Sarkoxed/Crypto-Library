from Crypto.Util.number import *
from math import sqrt, floor, ceil, gcd
from random import randint


def keygen(nbits: int):
    q = getRandomNBitInteger(nbits)
    while True:
        f = randint(1, floor(sqrt(q / 2)))
        g = randint(ceil(sqrt(q / 4)), floor(sqrt(q / 2)))
        if gcd(f, q * g) == 1:
            break

    h = (pow(f, -1, q) * g) % q
    return (f, g), (h, q)


def encrypt(h, q, m):
    assert m < sqrt(q / 4)

    r = randint(0, floor(sqrt(q / 2)))
    return (r * h + m) % q


def decrypt(f, g, q, e):
    a = (f * e) % q
    b = (pow(f, -1, g) * a) % g
    return b


if __name__ == "__main__":
    pri, pub = keygen(300)
    m = bytes_to_long(input("Your message: ").encode())
    e = encrypt(*pub, m)
    m = decrypt(*pri, pub[1], e)
    print(long_to_bytes(m))
