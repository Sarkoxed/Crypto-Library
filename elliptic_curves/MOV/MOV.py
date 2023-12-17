from sage.all import GF, EllipticCurve, discrete_log, floor, sqrt

from weil_pairing import weil_pairing


def MOV(P, Q, l: int):
    p = P.base_ring().order()
    assert l > floor(1 + sqrt(p))
    k = GF(l)(p).multiplicative_order()  # P.curve().embedding_degree()
    if k > 12:
        return None

    e = P.curve().change_ring(GF(p**k))
    N = e.order()
    while N % l == 0:
        N //= l

    g1, g2 = e.gens()
    g1 *= N
    g2 *= N

    while g1 * l != 0:
        g1 *= l

    while g2 * l != 0:
        g2 *= l

    if g1[0] in GF(p) and g1[1] in GF(p):
        T = g2
    else:
        T = g1

    a = weil_pairing(e(P), T, l)
    b = weil_pairing(e(Q), T, l)
    n = discrete_log(b, a)
    return n


def test():
    g = GF(691)
    e = EllipticCurve(g, [1, 0])
    p = e((301, 14))
    q = e((143, 27))
    n = MOV(p, q, 173)
    assert p * n == q


if __name__ == "__main__":
    test()
