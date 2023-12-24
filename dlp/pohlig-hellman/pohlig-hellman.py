from sage.all import GF, factor, gcd, randint


def easy_dlp(g, h, n):
    g0 = 1
    for i in range(n):
        if g0 == h:
            return i
        g0 *= g

    return None


def prime_power(g, h, p, n, k1):
    k = 0
    mult = 1
    for i in range(n - 1, -1, -1):
        h1, g1 = h, g
        for _ in range(i):
            h1 **= p
            g1 **= p

        ki = easy_dlp(g1, h1, p)
        h *= g ** (-ki)
        g **= p

        k += ki * mult
        mult *= p
        assert g ** ((k1 - k) // mult) == h
    return k


def test():
    p = 30877763578292445098700440347759436975049052128915248493103
    print(factor(p - 1))

    G = GF(p)
    g = G.multiplicative_generator() ** ((p - 1) // 101**10)
    assert g ** (101**10) == 1
    k = randint(1, 101**10 - 1)
    k //= gcd(k, 101**10)
    h = g**k

    m = prime_power(g, h, 101, 10, k)
    assert g**m == h


if __name__ == "__main__":
    test()
