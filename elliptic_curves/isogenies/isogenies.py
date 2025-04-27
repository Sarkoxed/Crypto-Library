from sage.all import (
    GF,
    EllipticCurve,
    EllipticCurve_from_j,
    PolynomialRing,
    classical_modular_polynomial,
    factor,
    lcm,
)


def get_polynomial_extension_degree(p):
    es = [f.degree() for f, _ in factor(p)]
    return lcm(es)


def get_all_isogenous_curves(E, l):
    assert l <= 3

    j = E.j_invariant()
    modular_F = classical_modular_polynomial(j=j, l=l).change_ring(E.base_ring())
    r = get_polynomial_extension_degree(modular_F)

    F = E.base_ring().extension(r)
    js = modular_F.change_ring(F).roots()
    return js


def get_all_isogenies(E, l):
    divpoly = E.division_polynomial(l).monic()
    # print(factor(divpoly3))
    r = get_polynomial_extension_degree(divpoly)

    F = E.base_ring().extension(r)
    G1, G2 = E.change_ring(F).torsion_basis(l)

    Kers = []
    for i in range(l):
        C = G1 + i * G2
        Ker = [j * C for j in range(l)]
        Kers.append(Ker)
    Kers.append([j * G2 for j in range(l)])

    res = [get_velu_isogeny(E, Ker) for Ker in Kers]
    _, cfs = list(zip(*res))

    js = []
    for A, B in cfs:
        j = 1728 * 4 * A**3 / (4 * A**3 + 27 * B**2)
        js.append(j)
    return js


def test_5():
    F = GF(11)
    E = EllipticCurve_from_j(F(3))
    print(get_all_isogenous_curves(E, 3))


if __name__ == "__main__":
    F = GF(101)
    E = EllipticCurve(F, [1, 13])

    print(get_all_isogenies(E, 3))
    print(get_all_isogenous_curves(E, 3))
    print()
    test_5()
