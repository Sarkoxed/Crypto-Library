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
