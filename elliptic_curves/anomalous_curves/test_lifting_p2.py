import pytest
from sage.all import GF, EllipticCurve, ZZ, Zmod
from random import randint

from lifting_p2 import solve_dlp_p2


def textbook_test():
    p = 853
    e = EllipticCurve(GF(p), [108, 4])

    P = e((0, 2))
    Q = e((563, 755))

    P1 = (0, 2)
    Q1 = (563, 66436)
    A1 = 7522715
    B1 = 4

    e2 = EllipticCurve(Zmod(p**2), [A1, B1])
    P2 = (p - 1) * e2(P1)
    Q2 = (p - 1) * e2(Q1)

    px2, py2 = [ZZ(x) for x in P2.xy()]
    qx2, qy2 = [ZZ(x) for x in Q2.xy()]

    m1 = p * (py2 - ZZ(P[1])) / (px2 - ZZ(P[0]))
    m2 = p * (qy2 - ZZ(Q[1])) / (qx2 - ZZ(Q[0]))

    k = (m1 / m2) % p
    assert P * k == Q

    assert k == solve_dlp_p2(108, 4, P, Q, 853)


@pytest.mark.parametrize("p, a, b, k", [(101, 1, 69, randint(1, 100))])
def test_nice(p, a, b, k):
    e = EllipticCurve(GF(p), [a, b])
    P = e.gens()[0]
    Q = k * P
    res = solve_dlp_p2(a, b, P, Q, p)
    while res is None:
        res = solve_dlp_p2(a, b, P, Q, p)
    assert res * P == Q
