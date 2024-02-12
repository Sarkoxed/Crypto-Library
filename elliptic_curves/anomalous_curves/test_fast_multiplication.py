import pytest
from sage.all import GF, EllipticCurve, is_prime
from random import randint

from fast_multiplication import mul_anom


@pytest.mark.parametrize("p, a, b, order", [(101, 1, 69, 2564871649947381046664216051)])
def test_nice(p, a, b, order):
    e = EllipticCurve(GF(p), [a, b])
    assert e.order() == p

    e = EllipticCurve(GF(p**25), [a, b])
    P = e.gens()[0] * (e.order() // order)
    assert P.order() == order
    assert is_prime(order)

    n = randint(1, order - 1)

    Pn = mul_anom(P, n, p)
    Pn1 = P * n
    assert Pn == Pn1
