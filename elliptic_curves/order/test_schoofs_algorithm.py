import pytest
from sage.all import GF, EllipticCurve, random_prime, PolynomialRing, var
from random import randint
from Crypto.Util.number import getPrime

from schoofs_algorithm import get_x1, get_y1_div_y, get_x_j, get_y_j_div_y, get_order
from division_polynomial import init_cache_noy, psi_cached_noy


def params_xy():
    p = random_prime(2**16)
    a = randint(0, p)
    b = randint(0, p)
    e = EllipticCurve(GF(p**2), [a, b])
    g = e.random_element()
    pl = randint(-g.order() // 2, g.order() // 2)
    return p, a, b, e, g, pl


@pytest.mark.parametrize("p, a, b, e, g, pl", [params_xy()])
def test_get_xy(p, a, b, e, g, pl):
    r1 = g + pl * g

    gx, gy = g.xy()
    cache = init_cache_noy(a, b, gx)
    t1, t2 = get_x1(gx, gx**3 + a * gx + b, cache, p**2, pl)
    w1, w2 = get_y1_div_y(gx, gx**3 + a * gx + b, t1, t2, cache, p, pl)
    x11, y11 = (t1 / t2, w1 / w2 * gy)

    assert e((x11, y11)) == r1


@pytest.mark.parametrize("a, b, p, l_prime", [(2, 1, 19, 5)])
def test_j_exists(a, b, p, l_prime):
    x = var("x")
    P = PolynomialRing(GF(p), x)
    cache = init_cache_noy(a, b, P(x))
    psi_l = psi_cached_noy(l_prime, cache, P(x**3 + a * x + b))

    e = EllipticCurve(GF(p**12), [a, b])
    g = e.gens()[1] * (e.order() // 25)
    assert g.order() == 5
    gx, gy = g.xy()
    assert psi_l(x=gx) == 0

    Q = P.quotient(psi_l)
    cache1 = init_cache_noy(a, b, Q(x))
    x1_num, x1_den = get_x1(Q(x), Q(x**3 + a * x + b), cache1, p, -1)
    x_j_num, x_j_den = get_x_j(Q(x), Q(x**3 + a * x + b), cache1, 2)
    x_q_j_num = x_j_num**p
    x_q_j_den = x_j_den**p

    res_num = x1_num * x_q_j_den - x1_den * x_q_j_num
    assert res_num == 0

    y1_num, y1_den = get_y1_div_y(
        Q(x), Q(x**3 + a * x + b), x1_num, x1_den, cache1, p, -1
    )
    y_j_num, y_j_den = get_y_j_div_y(Q(x), Q(x**3 + a * x + b), cache1, 2)
    y_q_j_num = y_j_num**p * Q(x**3 + a * x + b) ** ((p - 1) // 2)
    y_q_j_den = y_j_den**p

    # res_num = y1_num * y_q_j_den - y1_den * y_q_j_num
    res_num = y1_num * y_q_j_den + y1_den * y_q_j_num
    assert res_num == 0


def order_params(nbit):
    p = getPrime(nbit)
    a = randint(0, p)
    b = randint(0, p)
    return p, a, b


@pytest.mark.parametrize("p, a, b", [order_params(60)])
def test_order(p, a, b):
    e = EllipticCurve(GF(p), [a, b])
    assert get_order(a, b, p) == e.order()


@pytest.mark.parametrize("p, a, b, order", [(19, 2, 1, 27)])
def test_textbook(p, a, b, order):
    assert get_order(a, b, p) == order
