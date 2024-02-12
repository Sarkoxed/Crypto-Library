import pytest
from sage.all import GF, EllipticCurve

from MOV import MOV


@pytest.mark.parametrize(
    "p, a, b, px, py, qx, qy, order", [(691, 1, 0, 301, 14, 143, 27, 173)]
)
def test(p, a, b, px, py, qx, qy, order):
    g = GF(p)
    e = EllipticCurve(g, [a, b])
    p = e((px, py))
    q = e((qx, qy))
    m = MOV(p, q, order)
    assert p * m == q
