from sage.all import PolynomialRing, GF, Zmod, var, ZZ
from random import randrange
import logging


def lift(f, r, p, e):
    assert f.base_ring() is ZZ

    D = f.derivative()(x=r)
    if D % p == 0:
        if f(x=r) % p ** (e + 1) == 0:
            if p > 2**16:
                # logging.error("Too many extra roots, I'll just return 5 random ones")
                return [r + randrange(p) * p**e for _ in range(5)]
            return [r + i * p**e for i in range(p)]
        # logging.error(f"No roots that are = {r} mod p^{e} found mod p^{e + 1}")
        return []

    scale = f(x=r) // p**e
    t = -scale * pow(D, -1, p) % p
    return [r + t * p**e]


if __name__ == "__main__":
    F = PolynomialRing(ZZ, "x")
    x = F.gen()

    f = x**3 + 4 * x**2 + 7 * x + 1
    assert f(x=3) % 17 == 0
    r_2s = lift(f, 3, 17, 1)
    assert len(r_2s) == 1
    r_2 = r_2s[0]
    assert r_2 == 156
    assert f(x=r_2) % 17**2 == 0

    f = x**4 + 4902 * x**3 + 4844 * x**2 + 680 * x + 1100
    assert f(x=10) % 17 == 0
    r_2s = lift(f, 10, 17, 1)
    assert len(r_2s) == 17
    assert all(f(x=r) % 17**2 == 0 for r in r_2s)

    f = x**4 + 4902 * x**3 + 4844 * x**2 + 680 * x + 1100
    assert f(x=10) % 17**3 == 0
    r_2s = lift(f, 10, 17, 3)
    assert len(r_2s) == 0
    assert all(f(x=10 + i * 17**3) % 17**4 != 0 for i in range(17))
