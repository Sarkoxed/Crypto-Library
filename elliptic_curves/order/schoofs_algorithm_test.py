from schoofs_algorithm import *


def test_get_xy(n=1):
    from sage.all import GF, EllipticCurve, random_prime

    for _ in range(n):
        p = random_prime(2**16)
        a = randint(0, p)
        b = randint(0, p)
        e = EllipticCurve(GF(p**2), [a, b])
        g = e.random_element()
        pl = randint(-g.order() // 2, g.order() // 2)
        r1 = g + pl * g

        gx, gy = g.xy()
        cache = init_cache_noy(a, b, gx)
        t1, t2 = get_x1(gx, gx**3 + a * gx + b, cache, p**2, pl)
        w1, w2 = get_y1_div_y(gx, gx**3 + a * gx + b, t1, t2, cache, p, pl)
        x11, y11 = (t1 / t2, w1 / w2 * gy)

        assert e((x11, y11)) == r1


def test_j_exists():
    from sage.all import GF, EllipticCurve, random_prime

    a, b, p = 2, 1, 19
    l = 5
    x = var("x")
    P = PolynomialRing(GF(p), x)
    cache = init_cache_noy(a, b, P(x))
    psi_l = psi_cached_noy(l, cache, P(x**3 + a * x + b))

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


def test(n=1, nbit=50):
    from Crypto.Util.number import getPrime
    from sage.all import EllipticCurve, randint

    for _ in range(n):
        p = getPrime(nbit)
        a = randint(0, p)
        b = randint(0, p)
        e = EllipticCurve(GF(p), [a, b])
        print(e)

        assert get_order(a, b, p) == e.order()


def test_textbook():
    from sage.all import EllipticCurve

    p = 19
    a = 2
    b = 1
    print(get_order(a, b, p))


if __name__ == "__main__":
    test_get_xy(10)
    test_j_exists()
    test_textbook()
    test(10, 60)
