from sage.all import PolynomialRing, Zmod, GF, ZZ, Zp
from univariate_lifting import lift


def find_roots_hensel(f, p, e):
    assert f.base_ring() is ZZ

    P = PolynomialRing(Zmod(p**e), "x")
    if P(f) == 0:
        # NOTE this is very bad for big primes
        return list(range(p**e))
    del P

    if e == 1:
        P = PolynomialRing(GF(p), "x")
        return [int(r) for r, _ in P(f).roots()]

    base_roots = find_roots_hensel(f, p, e - 1)
    new_roots = []
    for r in base_roots:
        new_roots += lift(f, r, p, e - 1)

    assert len(new_roots) == len(set(new_roots))
    return new_roots


# May be faster, butd doesn't find all the roots on average
def find_roots_padic(f, p, e):
    assert f.base_ring() is ZZ
    F = Zp(p, e)
    P = PolynomialRing(F, "x")
    cfs = [F(c) for c in list(f)]
    f = P(cfs)
    return [ZZ(x) for x, _ in f.roots()]


# ----- Showcase -----


def showcase_root_finding_hensel():
    P = PolynomialRing(ZZ, "x")
    x = P.gen()
    f = x**4 + 4902 * x**3 + 4844 * x**2 + 680 * x + 1100

    aroots = sorted(find_roots_hensel(f, 17, 3))
    broots = [r for r in range(17**3) if f(x=r) % 17**3 == 0]
    assert aroots == broots

    aroots = find_roots_hensel(f, 17, 4)
    assert len(aroots) == 0

    assert all(f(r) % 17**4 != 0 for r in range(17**4))


def showcase_quad_mod_2_512():
    a, b, c = (
        3725667080359828237882050012075826816955394805983654212498828336484384511666451481428068119075593185083180437875735363631436104722896976357798815848393713,
        7040767378997130292683135402896235936138642309599829904422024790998920563606970660691438661815148117829535993274636456449028162117297789377809206699511724,
        8140090762026074454436391565007844730475305319076269374784087949381460619403420532213096947981591769170920654132599353795767443000632094692947790049687091,
    )

    P = PolynomialRing(ZZ, "x")
    x = P.gen()
    f = a * x**2 + b * x + c

    roots_hensel = find_roots_hensel(f, 2, 512)
    print(f"Hensel: Roots of {f} % 2^512")
    print(roots_hensel)
    assert all(f(x=r) % 2**512 == 0 for r in roots_hensel)
    print()

    roots_padic = find_roots_padic(f, 2, 512)
    print(f"Padic : Roots of {f} % 2^512")
    print(roots_padic)
    assert all(f(x=r) % 2**512 == 0 for r in roots_padic)
    print("=" * 50)
    print()


def showcase_quad_mod_2_64():
    a, b, c = 1, 0, -(1469416470735442835 + 1337**2)

    P = PolynomialRing(ZZ, "x")
    x = P.gen()
    f = a * x**2 + b * x + c

    roots_hensel = find_roots_hensel(f, 2, 64)
    print(f"Hensel: Roots of {f} % 2^64")
    print(roots_hensel)
    assert all(f(x=r) % 2**64 == 0 for r in roots_hensel)
    print()

    roots_padic = find_roots_padic(f, 2, 64)
    print(f"Padic : Roots of {f} % 2^64")
    print(roots_padic)
    assert all(f(x=r) % 2**64 == 0 for r in roots_padic)
    print("=" * 50)
    print()


def showcase_quad_mod_p_2():
    p = 156210697680525395807405913022225672867518230561026244167727827986872503969390713836672476231008571999805186039701198600755110769232069683662242528076520947841356681828813963095451798586327341737928960287475043247361498716148634925701665205679014796308116597863844787884835055529773239054412184291949429135511
    a, b, c = 1, -1, -1

    P = PolynomialRing(ZZ, "x")
    x = P.gen()
    f = a * x**2 + b * x + c

    roots_hensel = find_roots_hensel(f, p, 2)
    print(f"Hensel: Roots of {f} % p^2")
    print(roots_hensel)
    assert all(f(x=r) % p**2 == 0 for r in roots_hensel)
    print()

    roots_padic = find_roots_padic(f, p, 2)
    print(f"Padic : Roots of {f} % p^2")
    print(roots_padic)
    assert all(f(x=r) % p**2 == 0 for r in roots_padic)
    print("=" * 50)
    print()


if __name__ == "__main__":
    showcase_root_finding_hensel()
    showcase_quad_mod_2_512()
    showcase_quad_mod_2_64()
    showcase_quad_mod_p_2()
