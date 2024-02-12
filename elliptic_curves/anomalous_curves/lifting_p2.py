from sage.all import GF, QQ, ZZ, EllipticCurve, Zmod, crt, gcd, randint


def lift(A, B, P, Q, p):
    x1 = int(P[0]) + p * randint(0, p)
    x2 = int(Q[0]) + p * randint(0, p)
    y1 = int(P[1]) + p * randint(0, p)

    if x1 % p != x2 % p:
        y2 = int(crt([int(Q[1]), y1], [p, abs(x2 - x1)]))
        # y2 = int(crt([Q[1], -y1], [p, abs(x2-x1)]))

        A1 = (y2**2 - y1**2) // (x2 - x1) - (x2**3 - x1**3) // (x2 - x1)
    else:
        x2 = x1
        A1 = int(A) + p * randint(0, p)

        if Q == P:
            y2 = y1
        else:
            y2 = -y1

    B1 = y1**2 - x1**3 - A1 * x1

    assert y1**2 == x1**3 + A1 * x1 + B1
    assert y2**2 == x2**3 + A1 * x2 + B1

    return A1, B1, (x1, y1), (x2, y2)


def find_power(x, p):
    r = 0
    while x % p == 0:
        x //= p
        r += 1
    return r


def solve_dlp_QQ(A, B, P, Q, p):
    A1, B1, P1, Q1 = lift(A, B, P, Q, p)
    x1, y1 = P1
    x2, y2 = Q1

    E1 = EllipticCurve(QQ, [A1, B1])
    P2 = p * E1(P1)
    Q2 = p * E1(Q1)

    r1 = find_power(P2[0].denominator(), p)
    r2 = find_power(P2[1].denominator(), p)
    assert r1 * 3 - r2 * 2 == 0

    r1 = find_power(Q2[0].denominator(), p)
    r2 = find_power(Q2[1].denominator(), p)
    assert r1 * 3 - r2 * 2 == 0

    if (
        find_power(P2[0].denominator(), p) >= 4
        and find_power(P2[1].denominator(), p) >= 6
    ):  # P2 \in E_2
        return None

    l1 = (P2[0] / P2[1] / p) % p**4
    l2 = (Q2[0] / Q2[1] / p) % p**4
    return (l2 / l1) % p


def solve_dlp_p2(A, B, P, Q, p):
    A1, B1, P1, Q1 = lift(A, B, P, Q, p)
    x1, y1 = P1
    x2, y2 = Q1

    E1 = EllipticCurve(Zmod(p**2), [A1, B1])
    P2 = (p - 1) * E1(P1)
    Q2 = (p - 1) * E1(Q1)

    x3, y3 = ZZ(P2[0]), ZZ(P2[1])
    x4, y4 = ZZ(Q2[0]), ZZ(Q2[1])

    if x3 == x1 or x4 == x2:
        return None

    m1 = p * (y3 - y1) / (x3 - x1)  # or just m1 / m2 without *p
    m2 = p * (y4 - y2) / (x4 - x2)
    if gcd(m1.denominator(), p) != 1 or gcd(m2.denominator(), p) != 1:
        return None

    return (m1 / m2) % p
