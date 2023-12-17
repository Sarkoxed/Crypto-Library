from Crypto.Util.number import getPrime
from sage.all import GF, ceil, floor, gcd, randint, sqrt


def babystep_giantstep(g, h):
    gf = g.base_ring()
    n = g.multiplicative_order()
    m = 1 + ceil(sqrt(n))

    lg = {}
    gi = 1
    for i in range(m):
        lg[gi] = i
        gi *= g

    invg = g ** (-m)
    lh = [h]
    hi = h
    for j in range(m + 1):
        if hi in lg:
            i = lg[hi]
            return i + j * m
        hi *= invg


def birthday_algo(g, h):
    n = g.multiplicative_order()
    m = floor(3 * sqrt(n))

    gs = {}
    hs = {}
    flag = True

    for i in range(m):
        a = randint(0, n)
        ga = pow(g, a)
        gs[ga] = a

        if ga in hs:
            return a - hs[ga]  # not modded

        a = randint(0, n)
        ha = pow(g, a) * h
        hs[ha] = a

        if ha in gs:
            return gs[ha] - a


def test(n=1, nbit=20):
    p = getPrime(nbit // n)
    G = GF(p**n)

    g = G.random_element()
    N = g.multiplicative_order()

    k = randint(1, N - 1)
    k /= gcd(k, N)
    h = g**k

    k1 = babystep_giantstep(g, h)
    assert g**k1 == h

    k2 = birthday_algo(g, h)
    assert g**k2 == h


if __name__ == "__main__":
    test(n=2, nbit=40)
