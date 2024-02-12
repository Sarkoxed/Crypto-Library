from sage.all import random_prime, EllipticCurve, GF
import pytest
from random import randint

from supersingular import fast_multiplication, is_supersingular_legendre


def get_params():
    p = random_prime(2**20)
    while p % 3 != 2:
        p = random_prime(2**20)
    n = randint(1, p)
    return p, 0, 3, n


@pytest.mark.parametrize("p, a, b, n", [get_params()])
def test_multiplication(p, a, b, n):
    e = EllipticCurve(GF(p**5), [a, b])
    P = e.random_point()

    q = p**1
    Pn = fast_multiplication(P, n, q)
    Pn1 = P * n
    assert Pn == Pn1


@pytest.mark.parametrize("p, a, b", [(get_params()[0], 0, 2)])
def test_legendre(p, a, b):
    assert is_supersingular_legendre(a, b, p)


if __name__ == "__main__":
    test_multiplication()
    test_legendre()
