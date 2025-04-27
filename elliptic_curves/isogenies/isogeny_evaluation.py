from sage.all import GF, EllipticCurve, PolynomialRing, factor, lcm


# Weierstrass case
def get_velu_isogeny(E, Ker, x=None, iso=True):
    a, b = E.a4(), E.a6()

    C2, R = set(), set()
    for P in Ker:
        if P.order() == 1:
            continue
        if P.order() == 2:
            C2.add(P)
        elif -P not in R:
            R.add(P)

    F = E.base_ring()
    if x is None:
        Pf = PolynomialRing(F, "x")
        x = Pf.gens()[0]
    else:
        x = F(x)

    r_x, r_y = x, 1

    v_is = 0
    w_is = 0

    for Q in C2:
        Qx = Q[0]

        gx = 3 * Qx**2 + a
        v = gx

        if iso:
            r_x += v / (x - Qx)
            r_y -= v / (x - Qx) ** 2

        v_is += v
        w_is += Qx * v

    for Q in R:
        Qx, Qy = Q.xy()

        gx = 3 * Qx**2 + a
        gy = -2 * Qy

        v = 2 * gx
        u = gy**2

        if iso:
            r_x += v / (x - Qx) + u / (x - Qx) ** 2
            r_y -= 2 * u / (x - Qx) ** 3 + v / (x - Qx) ** 2

        v_is += v
        w_is += u + v * Qx

    A = a - 5 * v_is
    B = b - 7 * w_is
    if iso:
        return (r_x, r_y), (A, B)
    return (A, B)


def get_isogeny_of_smooth_order(E, K, l):
    assert K.order() == l
    assert all(p < 2**32 for p, _ in factor(l, limit=2**32))

    F = E.base_ring()
    K0 = K
    E0 = E
    for p, e in factor(l):
        for _ in range(e):
            K1 = K0 * (K0.order() // p)
            kernel = [k * K1 for k in range(p)]
            if K0.order() != p:
                isoK0, AB = get_velu_isogeny(E0, kernel, x=K0[0])
                E0 = EllipticCurve(F, AB)
                K0 = E0(isoK0[0], K0[1] * isoK0[1])
            else:
                AB = get_velu_isogeny(E0, kernel, iso=False)
                E0 = EllipticCurve(F, AB)
    return E0


def evaluate_isogeny_of_smooth_order(E, K, l, P):
    assert K.order() == l
    assert all(p < 2**32 for p, _ in factor(l, limit=2**32))
    assert P in E

    F = E.base_ring()
    K0 = K
    E0 = E
    for p, e in factor(l):
        for _ in range(e):
            K1 = K0 * (K0.order() // p)
            kernel = [k * K1 for k in range(p)]
            if K0.order() != p:
                isoK0, AB = get_velu_isogeny(E0, kernel, x=K0[0])
                Pxy, _ = get_velu_isogeny(E0, kernel, x=P[0])
                E0 = EllipticCurve(F, AB)
                K0 = E0(isoK0[0], K0[1] * isoK0[1])
            else:
                AB = get_velu_isogeny(E0, kernel, iso=False)
                Pxy, _ = get_velu_isogeny(E0, kernel, x=P[0])
                E0 = EllipticCurve(F, AB)
            P = E0(Pxy[0], P[1] * Pxy[1])
    return P


def test_3():
    F = GF(101)
    E = EllipticCurve(F, [1, 13])

    E1 = E.change_ring(F.extension(2))
    G1, G2 = E1.torsion_basis(3)

    Ker1 = [G1, -G1]
    Ker2 = [G2, -G2]
    Ker3 = [G1 + G2, -G1 - G2]
    Ker4 = [G1 - G2, -G1 + G2]

    isogeny, AB = get_velu_isogeny(E, Ker1)
    print(isogeny)


def test_4_isogeny_cycle():
    F = GF(101)
    E = EllipticCurve(F, [1, 13])

    E1 = E
    c = 0
    while True:
        c += 1
        G = E1.gens()[0] * (E1.gens()[0].order() // 3)
        assert G.order() != 1
        Ker = [G, -G]
        isogeny, AB = get_velu_isogeny(E1, Ker)
        E1 = EllipticCurve(F, AB)
        if E1 == E:
            break
        print(E1)
    print(f"Cycle length: {c}")


if __name__ == "__main__":
    test_3()
    print()
    test_4_isogeny_cycle()
