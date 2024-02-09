from sage.all import EllipticCurve, GF, QQ, var, divisors, sqrt, PolynomialRing, ZZ

def torsion_2_points(E):
    A, B = E.a4(), E.a6()
    x = var('x')
    Pr = PolynomialRing(QQ, x)
    roots = Pr(x**3 + A * x + B).roots(multiplicities=False) # assume not singular
    return [E((r, 0)) for r in roots]

# get possible torsion points(known factorization)
def lutz_nagell(E):
    A, B = E.a4(), E.a6()
    delt = 4 * A**3 + 27 * B**2
    desired = delt / delt.squarefree_part()
    possible_ys = divisors(sqrt(desired))
    
    x = var('x')
    Pr = PolynomialRing(QQ, x)
    rational_points = []
    for y in possible_ys:
        roots = Pr(x**3 + A * x + B - y**2).roots(multiplicities=False)
        for tmp_x in roots:
            rational_points.append(E((tmp_x, y)))
            rational_points.append(E((tmp_x, -y)))
    return rational_points

def is_torsion_point_mazur(P):
    P0 = P
    for i in range(1, 12 + 1):
        if P0 == 0:
            return True, i
        elif not (P0[0] in ZZ or P0[1] in ZZ):
            return False, None
        P0 += P

def torsion_subgroup_order(E, bound=1000):
    A, B = E.a4(), E.a6()
    delt = 4 * A**3 + 27 * B**2
    torsion_order = None
    for p in prime_range(bound):
        if delt % p == 0:
            continue
        E1 = E.change_ring(GF(p))
        N1 = E1.order()
        if torsion_order is None:
            torsion_order = N1
        else:
            torsion_order = gcd(torsion_order, N1)
    return torsion_order

def test():
    # cyclic
    E = EllipticCurve(QQ, [0, -2]) # order 0
    ptp = lutz_nagell(E) + torsion_2_points(E)
    assert len(ptp) == 0

    E = EllipticCurve(QQ, [0, 8]) # order 2
    ptp0 = set(torsion_2_points(E))
    ptp1 = set(lutz_nagell(E)) - ptp0
    assert len(ptp0) == 1
    assert not any(is_torsion_point_mazur(P)[0] for P in ptp1)

    E = EllipticCurve(QQ, [0, 4]) # order 3
    ptp0 = set(torsion_2_points(E))
    ptp1 = set(lutz_nagell(E)) - ptp0
    assert len(ptp0) == 0
    assert all(is_torsion_point_mazur(P)[1] == 3  for P in ptp1)

    E = EllipticCurve(QQ, [4, 0]) # order 4
    ptp0 = set(torsion_2_points(E))
    ptp1 = set(lutz_nagell(E)) - ptp0
    assert is_torsion_point_mazur(list(ptp1)[1])[1] == 4
 
    E = EllipticCurve(QQ, [-432, 8208]) # order 5
    ptp0 = set(torsion_2_points(E))
    ptp1 = set(lutz_nagell(E)) - ptp0
    assert len(ptp0) == 0
    assert is_torsion_point_mazur(list(ptp1)[0])[1] == 5

    E = EllipticCurve(QQ, [0, 1]) # order 6
    ptp0 = set(torsion_2_points(E))
    ptp1 = set(lutz_nagell(E)) - ptp0
    assert any(is_torsion_point_mazur(P)[1] == 6 for P in ptp1)
  
    E = EllipticCurve(QQ, [-1323, 6395814]) # order 7
    ptp0 = set(torsion_2_points(E))
    ptp1 = set(lutz_nagell(E)) - ptp0
    assert len(ptp0) == 0
    assert any(is_torsion_point_mazur(P)[1] == 7 for P in ptp1)

    E = EllipticCurve(QQ, [-44091, 3304854]) # order 8
    ptp0 = set(torsion_2_points(E))
    ptp1 = set(lutz_nagell(E)) - ptp0
    assert any(is_torsion_point_mazur(P)[1] == 8 for P in ptp1)
 
    E = EllipticCurve(QQ, [-219, 1654]) # order 9
    ptp0 = set(torsion_2_points(E))
    ptp1 = set(lutz_nagell(E)) - ptp0
    assert len(ptp0) == 0
    assert any(is_torsion_point_mazur(P)[1] == 9 for P in ptp1)

    E = EllipticCurve(QQ, [-58347, 3954150]) # order 10
    ptp0 = set(torsion_2_points(E))
    ptp1 = set(lutz_nagell(E)) - ptp0
    assert any(is_torsion_point_mazur(P)[1] == 10 for P in ptp1)

    E = EllipticCurve(QQ, [-33339627, 73697852646]) # order 12
    ptp0 = set(torsion_2_points(E))
    ptp1 = set(lutz_nagell(E)) - ptp0
    assert any(is_torsion_point_mazur(P)[1] == 12 for P in ptp1)


    # VSp
    E = EllipticCurve(QQ, [-1, 0]) # order 2x2
    ptp0 = set(torsion_2_points(E))
    ptp1 = set(lutz_nagell(E)) | ptp0
    orders = [is_torsion_point_mazur(P) for P in ptp1]
    assert any(x[1] == 2 for x in orders)
    assert all(x[1] != 4 for x in orders)
    assert sum([x[0] for x in orders]) == 4 - 1 # exclude oo
 
    E = EllipticCurve(QQ, [-12987, -263466]) # order 2x4
    ptp0 = set(torsion_2_points(E))
    ptp1 = set(lutz_nagell(E)) | ptp0
    orders = [is_torsion_point_mazur(P) for P in ptp1]
    assert any(x[1] == 2 for x in orders)
    assert any(x[1] == 4 for x in orders)
    assert all(x[1] != 8 for x in orders)
    assert sum([x[0] for x in orders]) == 8 - 1

    E = EllipticCurve(QQ, [-24003, 1296702]) # order 2x6
    ptp0 = set(torsion_2_points(E))
    ptp1 = set(lutz_nagell(E)) | ptp0
    orders = [is_torsion_point_mazur(P) for P in ptp1]
    assert any(x[1] == 2 for x in orders)
    assert any(x[1] == 6 for x in orders)
    assert all(x[1] != 12 for x in orders)
    assert sum([x[0] for x in orders]) == 12 - 1

    E = EllipticCurve(QQ, [-1386747, 368636886]) # order 2x8
    ptp0 = set(torsion_2_points(E))
    ptp1 = set(lutz_nagell(E)) | ptp0
    orders = [is_torsion_point_mazur(P) for P in ptp1]
    assert any(x[1] == 2 for x in orders)
    assert any(x[1] == 8 for x in orders)
    assert all(x[1] != 16 for x in orders)
    assert sum([x[0] for x in orders]) == 16 - 1

if __name__ == "__main__":
    test()
