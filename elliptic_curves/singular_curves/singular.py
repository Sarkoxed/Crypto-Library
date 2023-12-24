from sage.all import GF, EllipticCurve, PolynomialRing, randint, random_prime, var


def add(P, Q, a):
    if P[2] == 0:
        return Q
    elif Q[2] == 0:
        return P
    if Q[1] == -P[1]:
        return (0, 1, 0)

    if P != Q:
        l = (Q[1] - P[1]) / (Q[0] - P[0])
    else:
        l = (3 * P[0] ** 2 + a) / (2 * P[1])

    x3 = l**2 - P[0] - Q[0]
    y3 = -l * (x3 - P[0]) - P[1]
    return (x3, y3, 1)


def mul(P, n: int, a):
    R0, R1 = P, add(P, P, a)
    for i in bin(n)[3:]:
        if i == "0":
            R0, R1 = add(R0, R0, a), add(R0, R1, a)
        else:
            R0, R1 = add(R0, R1, a), add(R1, R1, a)
    return R0


def single_root():
    # y**2 = x**3 mod p
    p = random_prime(2**128)
    G = GF(p)

    gx = G.random_element()
    while not (gx**3).is_square():
        gx = G.random_element()

    gy = (gx**3).sqrt()
    assert gy**2 == gx**3

    P = (gx, gy, 1)
    k = randint(0, p)
    Q = mul(P, k, 0)
    assert Q[1] ** 2 == Q[0] ** 3

    alpha = gx / gy
    beta = Q[0] / Q[1]
    k1 = beta / alpha
    assert k == k1


def translate(a0, a1, a2, gx, p):
    x = var("x")
    G = GF(p)
    a0, a1, a2 = int(a0), int(a1), int(a2)
    gx = G(gx)

    P = PolynomialRing(GF(p), x)
    poly = P(x**3 + a2 * x**2 + a1 * x + a0)

    sub = G(a2) / G(3)
    gx = gx + sub
    poly = poly(x=P(x) - int(sub))

    B, A = poly.coefficients()[:-1]
    return gx, A, B


def double_root_square():
    # y^2 = x^2(x + a)
    p = 4368590184733545720227961182704359358435747188309319510520316493183539079703
    G = GF(p)

    a = G.random_element()
    while not a.is_square():
        a = G.random_element()

    gx = G.random_element()
    while not (gx**2 * (gx + a)).is_square():
        gx = G.random_element()
    gy = (gx**3 + a * gx**2).sqrt()
    gx, A, B = translate(0, 0, a, gx, p)

    P = (gx, gy, 1)
    k = randint(1, p - 1)
    Q = mul(P, k, A)

    assert P[0] ** 3 + A * P[0] + B == P[1] ** 2
    assert Q[0] ** 3 + A * Q[0] + B == Q[1] ** 2

    x = var("x")
    Pr = PolynomialRing(GF(p), x)
    r1, r2 = Pr(x**3 + int(A) * x + int(B)).roots(multiplicities=False)
    assert r1**3 + A * r1 + B == 0
    assert r2**3 + A * r2 + B == 0
    assert 3 * r2**2 + A == 0
    assert (P[0] - r1) * (P[0] - r2) ** 2 == P[1] ** 2
    assert (Q[0] - r1) * (Q[0] - r2) ** 2 == Q[1] ** 2

    P = (P[0] - r2, P[1], 1)
    Q = (Q[0] - r2, Q[1], 1)
    r1 = r2 - r1

    assert P[0] ** 2 * (P[0] + r1) == P[1] ** 2
    assert Q[0] ** 2 * (Q[0] + r1) == Q[1] ** 2
    assert r1.is_square()

    al = r1.sqrt()
    alpha = (P[1] + al * P[0]) / (P[1] - al * P[0])
    beta = (Q[1] + al * Q[0]) / (Q[1] - al * Q[0])

    k1 = beta.log(alpha)
    assert alpha**k1 == beta


def double_root_not_square():
    # y^2 = x^2(x + a)
    p = 1121176762756766432968019
    G = GF(p)

    a = G.random_element()
    while a.is_square():
        a = G.random_element()

    gx = G.random_element()
    while not (gx**2 * (gx + a)).is_square():
        gx = G.random_element()
    gy = (gx**3 + a * gx**2).sqrt()
    gx, A, B = translate(0, 0, a, gx, p)

    P = (gx, gy, 1)
    k = randint(1, p - 1) * 3242247097191079
    Q = mul(P, k, A)

    assert P[0] ** 3 + A * P[0] + B == P[1] ** 2
    assert Q[0] ** 3 + A * Q[0] + B == Q[1] ** 2

    x = var("x")
    Pr = PolynomialRing(GF(p), x)
    r1, r2 = Pr(x**3 + int(A) * x + int(B)).roots(multiplicities=False)
    assert r1**3 + A * r1 + B == 0
    assert r2**3 + A * r2 + B == 0
    assert 3 * r2**2 + A == 0
    assert (P[0] - r1) * (P[0] - r2) ** 2 == P[1] ** 2
    assert (Q[0] - r1) * (Q[0] - r2) ** 2 == Q[1] ** 2

    P = (P[0] - r2, P[1], 1)
    Q = (Q[0] - r2, Q[1], 1)
    r1 = r2 - r1

    assert P[0] ** 2 * (P[0] + r1) == P[1] ** 2
    assert Q[0] ** 2 * (Q[0] + r1) == Q[1] ** 2
    assert not r1.is_square()

    al = GF(p**2)(r1).sqrt()
    alpha = (P[1] + al * P[0]) / (P[1] - al * P[0])
    beta = (Q[1] + al * Q[0]) / (Q[1] - al * Q[0])
    assert alpha**k == beta

    k1 = beta.log(alpha)
    assert alpha**k1 == beta


if __name__ == "__main__":
    single_root()
    double_root_square()
    double_root_not_square()
