from sage.all import GF, EllipticCurve, discrete_log


def g_direct(P, Q, R):
    xp, yp = P.xy()
    xq, yq = Q.xy()
    xr, yr = R.xy()

    if P == -Q:
        return xr - xp

    a4 = P.curve().a4()
    if P != Q:
        l = (yq - yp) / (xq - xp)
    else:
        l = (a4 + 3 * xp**2) / (2 * yp)

    return (yr - yp - l * (xr - xp)) / (xr + xp + xq - l**2)


def MillerAlgorithm_direct(P, Q, m: int):
    T, f = P, 1
    for b in bin(m)[3:]:
        f = f * f * g_direct(T, T, Q)
        T += T
        if b == "1":
            f = f * g_direct(T, P, Q)
            T += P
    return f


def weil_pairing(P, Q, l: int, S=None):
    if S is None:
        S = P.curve().random_point()
        while S * l == 0:
            S = P.curve().random_point()

    fp_num = MillerAlgorithm_direct(P, Q + S, l)
    fp_den = MillerAlgorithm_direct(P, S, l)
    fp = fp_num / fp_den

    fq_num = MillerAlgorithm_direct(Q, P - S, l)
    fq_den = MillerAlgorithm_direct(Q, -S, l)
    fq = fq_num / fq_den

    return fp / fq


def test_textbook():
    e = EllipticCurve(GF(631), [30, 34])
    p = e((36, 60))
    q = e((121, 387))
    s = e((0, 36))

    res = set()
    for _ in range(e.order()):
        d = weil_pairing(p, q, 5, s)
        res.add(d)
    assert len(res) == 1
    assert list(res)[0] ** 5 == 1
    assert list(res)[0] == 242
    assert p.weil_pairing(q, p.order()) == 242


def test_error():
    g = GF(691)
    e = EllipticCurve(g, [1, 0])
    p = e((301, 14))
    q = e((143, 27))

    l = p.order()
    assert q * l == 0
    assert q == 122 * p

    assert weil_pairing(p, q, l) == 1


if __name__ == "__main__":
    test_textbook()
    test_error()
