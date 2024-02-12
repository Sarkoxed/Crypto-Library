from sage.all import factor, GF, randint, gcd

from pohlig_hellman import prime_power


def test():
    p = 30877763578292445098700440347759436975049052128915248493103

    G = GF(p)
    g = G.multiplicative_generator() ** ((p - 1) // 101**10)
    assert g ** (101**10) == 1
    k = randint(1, 101**10 - 1)
    k //= gcd(k, 101**10)
    h = g**k

    m = prime_power(g, h, 101, 10, k)
    assert g**m == h
