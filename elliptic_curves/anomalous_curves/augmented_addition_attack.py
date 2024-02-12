from sage.all import GF, ZZ, EllipticCurve, Qp, randint, random_prime


def mul(P, n):
    if n < 0:
        P = -P
        n = -n
    b = bin(n)[2:]
    Q = P
    for i in b[1:]:
        Q = add(Q, Q)
        if i == "1":
            Q = add(Q, P)
    return Q


def a0(P, Q):
    if P.is_zero() or Q.is_zero() or P == -Q:
        return 0

    if P == Q:
        t = P.curve().a4()
        return (3 * P[0] ** 2 + t) * pow(2 * P[1], -1)

    return (P[1] - Q[1]) * pow(P[0] - Q[0], -1)


def add(P, Q):
    p1, scal1 = P
    p2, scal2 = Q
    p3 = p1 + p2
    scal3 = scal1 + scal2 + a0(p1, p2)
    return p3, scal3
