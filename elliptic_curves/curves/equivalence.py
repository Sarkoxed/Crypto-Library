from sage.all import GF, EllipticCurve, var, PolynomialRing
from edwards_curve import Edwards, EPoint 
from montgomery_curve import Montgomery, MPoint

def montgomery_to_edwards_curve(M: Montgomery):
    a = ((M.a + 2) * pow(M.b, -1, M.p)) % M.p
    d = ((M.a - 2) * pow(M.b, -1, M.p)) % M.p
    return Edwards(M.p, a, d)

def montgomery_to_edwards_point(P: MPoint):
    E = montgomery_to_edwards_curve(P.E)
    x = (P.x * pow(P.y, -1, E.p)) % E.p
    y = ((P.x - 1) * pow(P.x + 1, -1, E.p)) % E.p
    return EPoint(x, y, E)

def montgomery_to_weierstrass_curve(M: Montgomery):
    a = ((3 - M.a**2) * pow(3 * M.b**2, -1, M.p)) % M.p
    b = ((2 * M.a**3 - 9 * M.a) * pow(27 * M.b**3, -1, M.p)) % M.p
    return EllipticCurve(GF(M.p), [a, b])

def montgomery_to_weierstrass_point(P: MPoint):
    E = montgomery_to_weierstrass_curve(P.E)

    p = P.E.p
    g = GF(p)

    x = g(P.x) / g(P.E.b) + g(P.E.a) / g(3 * P.E.b)
    y = g(P.y) / g(P.E.b)
    return E((x, y)) 

def edwards_to_montgomery_curve(Ed: Edwards):
    a = (2 * (Ed.a + Ed.d) * pow(Ed.a - Ed.d, -1, Ed.p)) % Ed.p
    b = (4 * pow(Ed.a - Ed.d, -1, Ed.p)) % Ed.p
    return Montgomery(Ed.p, b, a)

def edwards_to_montgomery_point(EP: EPoint):
    M = edwards_to_montgomery_curve(EP.E)
    x = ((1 + EP.y) * pow(1 - EP.y, -1, M.p)) % M.p
    y = ((1 + EP.y) * pow((1 - EP.y) * EP.x, -1, M.p)) % M.p
    return MPoint(x, y, M)

def weierstrass_to_montgomery_curve(E: EllipticCurve, flag = True):
    if E.order() % 4 != 0:
        return None
    
    x = var('x')
    Pt = PolynomialRing(E.base_field(), x)

    a = int(E.a4())
    b = int(E.a6())
    
    r = Pt(x**3 + a * x + b).roots()
    if len(r) == 0:
        return None
    
    alpha = None
    for x, _ in r:
        if pow(3 * x**2 + a, (E.base_field().order() - 1)/2) == 1:
            alpha = x
            break

    if alpha is None:
        return None

    s = (3 * alpha**2 + a).sqrt()**(-1)
    if flag:
        s = -s

    A = int(3 * alpha * s)
    B = int(s)

    return Montgomery(E.base_field().order(), B, A)

def weierstrass_to_montgomery_point(G, flag=True):
    M = weierstrass_to_montgomery_curve(G.curve())
    if M is None:
        return None

    a = int(G.curve().a4())
    b = int(G.curve().a6())

    x = var('x')
    Pt = PolynomialRing(G.curve().base_field(), x)
    r = Pt(x**3 + a * x + b).roots()
    alpha = None
    for x, _ in r:
        if pow(3 * x**2 + a, (G.curve().base_field().order() - 1)/2) == 1:
            alpha = x
            break
    s = (3 * alpha**2 + a).sqrt()**(-1)
    if flag:
        s = -s

    t, v = G.xy()
    
    res = None
    x = int(s * (t - alpha))
    y = int(s * v)
    return MPoint(x, y, M)
    
if __name__ == "__main__":
    p = 2**255 - 19
    a = -1
    c = 1
    d = 0x52036cee2b6ffe738cc740797779e89800700a4d4141d8ab75eb4dca135978a3
    n = 0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3ed
    E = Edwards(p, a, d, c)
    G = EPoint(0x216936d3cd6e53fec0a4e231fdd6dc5c692cc7609525a7b2c9562d608f25d51a, 0x6666666666666666666666666666666666666666666666666666666666666658, E)
    print(G * n)

    M = edwards_to_montgomery_curve(E)
    print(f"M = {M.a, M.b}")
    GM = edwards_to_montgomery_point(G)

    print(GM * n)

    W = montgomery_to_weierstrass_curve(M)
    print(W)
    GW = montgomery_to_weierstrass_point(GM)

    print(GW * n)

    M1 = weierstrass_to_montgomery_curve(W, True)
    GM1 = weierstrass_to_montgomery_point(GW, True)
