from sage.all import log, EllipticCurve, QQ

def Hn(x):
    return max(abs(x.numerator()), abs(x.denominator()))

def hn(x):
    return log(H(x))

def H(P):
    if P == 0:
        return 1
    x = P[0]
    return Hn(x)

def h(P):
    return log(H(P[0]))

def canonical_h(P, bound=10):
    return h(2**bound * P) / 4**bound / 2

def canonical_h_iter(P, bound=10):
    P, P1 = P, P
    h_res = h(P).n()
    for j in range(1, bound+1):
        P, P1 = P1, 2 * P1
        h_res += (h(P1).n() - 4 * h(P).n()) / 4**j
    return h_res / 2

def silverman_bounds(E):
    A, B = E.a4(), E.a6()
    delta = -16 * (4 * A**3 + 27*B**3)
    j = -1728 * (4 * A)**3 / delta
    left_bound = -hn(j) / 8  - hn(delta) / 12 - 0.973
    right_bound = hn(j) / 12 + hn(delta) / 12 + 1.07
    return (left_bound.n(), right_bound.n())

def height_pairing(P, Q, bound=10):
    return canonical_h(P + Q, bound) - canonical_h(P, bound) - canonical_h(Q, bound)

def test():
    E = EllipticCurve(QQ, [-25, 0])
    P = E((-4, 6))
    n = 5
    print((canonical_h(n*P, bound=9) / canonical_h(P, bound=9)).n())

if __name__ == "__main__":
    test()
