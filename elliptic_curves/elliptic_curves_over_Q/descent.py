from sage.all import EllipticCurve, QQ, var

def get_all_triples(E):
    A, B = E.a4(), E.a6()
    x = var('x')
    Pr = PolynomialRing(QQ, x)
    e3, e2, e1 = Pr(x**3 + A * x + B).roots(multiplicities=False) # e1 < e2 < e3
    tmp = (e1 - e2) *  (e1 - e3) * (e2 - e3)
    S = divisors(product(ZZ(tmp).prime_divisors()))
    
    triples = []
    for a in S:   
        for b in S:
            triples.append((a, b, (a * b).squarefree_part()))
            triples.append((-a, -b, (a * b).squarefree_part()))
    return (e1, e2, e3), triples

def phi(P, es):
    e1, e2, e3 = es
    
    if P == 0:
        res = (1, 1, 1)
    elif P[0] == e1:
        res ((e1 - e2) * (e1 - e3), e1 - e2, e1 - e3)
    elif P[0] == e2:
        res (e2 - e1, (e2 - e1) * (e2 - e3), e2 - e3)
    elif P[0] == e3:
        res (e3 - e1, e3 - e2, (e3 - e1) * (e3 - e2))
    else:
        res = (P[0] - e1, P[0] - e2, P[0] - e3)
    return (res[0].squarefree_part(), res[1].squarefree_part(), res[2].squarefree_part())

# TODO: extend to the K/Q - finite extension, Ok - ring of algebraic integers
