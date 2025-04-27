from sage.all import QQ, PolynomialRing, expand
from itertools import permutations

# everything could be done using SymmetricFunctions but whatever
# Thanks https://www.youtube.com/watch?v=50pXtgintLc&ab_channel=diplomaticfish


def get_poly(gens, powers):
    res_poly = 0
    for power in powers:
        assert len(power) == len(gens)
        monomial = 1
        for g, alpha in zip(gens, power):
            monomial *= g**alpha
        res_poly += monomial
    return res_poly


def get_basis(gens):
    n = len(gens)

    basis_polys = []
    for k in range(1, n + 1):
        monomial = [1 for _ in range(k)] + [0 for _ in range(n - k)]
        poly_powers = list(set(permutations(monomial)))  # avoiding duplicates
        basis_polys.append(get_poly(gens, poly_powers))
    return basis_polys


def decompose(f, basis):
    n = len(basis)
    f = expand(f)
    assert f.is_symmetric()

    sym_basis = list(PolynomialRing(QQ, n, "s").gens())

    dec = 0
    while not f.is_constant():
        tmp = [(c[0], c[1].degrees()) for c in list(f)]
        cf, degree = max(tmp, key=lambda x: x[1])

        assert tuple(sorted(degree, reverse=True)) == degree  # sym check

        tmpoly = 1
        tmpsym = 1
        for k in range(1, n):
            curpower = degree[k - 1] - degree[k]
            tmpoly *= basis[k - 1] ** curpower
            tmpsym *= sym_basis[k - 1] ** curpower

        tmpoly *= basis[-1] ** degree[-1]
        tmpsym *= sym_basis[-1] ** degree[-1]

        tmpoly *= cf
        tmpsym *= cf

        f -= tmpoly
        dec += tmpsym
    dec += int(f)
    return dec


def test():
    P = PolynomialRing(QQ, 3, "x")
    gens = list(P.gens())
    print(gens)

    basis = get_basis(gens)

    x0, x1, x2 = gens
    for n in range(1, 5):
        f = P(x0**n + x1**n + x2**n)

        dec = decompose(f, basis)
        print(dec)


if __name__ == "__main__":
    test()
