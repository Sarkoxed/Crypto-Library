from sage.all import EllipticCurve, QQ, exp, ceil, var, PolynomialRing, ZZ, Matrix
from height import silverman_bounds, h, hn, canonical_h, canonical_h_iter
from torsion_subgroup import torsion_2_points, lutz_nagell

def find_points_height(E, c):
    M = ceil(exp(c))
    print(f"Bound: {M}")
    A, B = E.a4(), E.a6()
    
    found_points = []
    for a in range(-M, M+1):
        for b in range(1, M+1):
            x = ZZ(a) / ZZ(b)
            ysq = x**3 + A * x + B
            if ysq.is_square():
                P = E.lift_x(x)
                if P not in found_points:
                    found_points.append(P)
                    print(P)
                    if P[1] != 0:
                        found_points.append(-P)
    return found_points

E = EllipticCurve(QQ, [-25, 0])
t2 = set(torsion_2_points(E))
#ptp = lutz_nagell(E)

h = canonical_h(E((-4, 6))).n()
left, right = silverman_bounds(E)
hb = (-left + h) * 2

ph = set(find_points_height(E, hb)) - t2

M = Matrix([[]])
