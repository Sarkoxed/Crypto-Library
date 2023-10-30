from sage.all import Zmod, GF, PolynomialRing, ZZ, var, gcd, Zp


def find_root(cfs, p, exp, comp_bound=10**8):
    x = var("x")
    P = PolynomialRing(GF(p), x)
    zz_poly = PolynomialRing(ZZ, x)(cfs)
    poly = P(cfs)
    cure = 1
    while poly == 0:
        cure += 1
        P = PolynomialRing(Zmod(p**cure), x)
        poly = P(cfs)

    roots = []
    print(roots)
    if cure == 1:
        roots = poly.roots()
        if len(roots) == 0:
            return []
        roots = [int(r[0]) for r in roots]
    else:
        if p**cure < comp_bound:
            for r in range(0, p**cure):
                if poly(x=r) == 0 and poly.derivative()(x=r) != 0:
                    roots.append(r)

    for e in range(cure + 1, exp + 1):
        newroots = []
        for r in roots:
            if zz_poly.derivative()(x=r) % p != 0:
                a = -(zz_poly(x=r) // p**cure)
                b = pow(
                    zz_poly.derivative()(x=r), -1, p
                )
                t = (a * b) % p
                newroots.append(int((r + t * p**cure) % p ** (cure + 1)))
            elif (zz_poly(x=r) // p**cure) % p == 0:
                for k in range(p):
                    tmp = int((r + k * p**cure) % p ** (cure + 1))
                    assert poly(x=tmp) == 0
                    newroots.append(tmp)

        roots = newroots
        cure += 1
        poly = zz_poly.change_ring(Zmod(p**cure))
#    print(roots)
    return roots
# TODO compare to https://github.com/gmossessian/Hensel

def padic_roots(cfs, p, e):
    cfs = [Zp(p, e)(c) for c in cfs]
    R = Zp(p, e)
    P = PolynomialRing(R, 'x')
    poly = P(cfs)
#    print(poly)
    return [ZZ(x) for x, _ in poly.roots()]

if __name__ == "__main__":
    a, b, c = (
        3725667080359828237882050012075826816955394805983654212498828336484384511666451481428068119075593185083180437875735363631436104722896976357798815848393713,
        7040767378997130292683135402896235936138642309599829904422024790998920563606970660691438661815148117829535993274636456449028162117297789377809206699511724,
        8140090762026074454436391565007844730475305319076269374784087949381460619403420532213096947981591769170920654132599353795767443000632094692947790049687091,
    )
    
    roots_hensel = find_root([c, b, a], 2, 512)
    print(roots_hensel)
    
    for r in roots_hensel:
        assert (a * r**2 + b * r + c) % 2**512 == 0
    
    roots_padic = padic_roots([c, b, a], 2, 512)
    print(roots_padic)
    
    for r in roots_padic:
        assert (a * r**2 + b * r + c) % 2**512 == 0
    
    a, b, c = 1, 0, -(1469416470735442835 + 1337**2)
    
    roots_hensel = find_root([c, b, a], 2, 64)
    print(roots_hensel)
    
    
    roots_padic = padic_roots([c, b, a], 2, 64)
    print(roots_padic)
    
    a, b, c = 1, -1, -1
    p = 156210697680525395807405913022225672867518230561026244167727827986872503969390713836672476231008571999805186039701198600755110769232069683662242528076520947841356681828813963095451798586327341737928960287475043247361498716148634925701665205679014796308116597863844787884835055529773239054412184291949429135511
    
    roots_hensel = find_root([c, b, a], p, 2)
    print(roots_hensel)
    
    roots_hensel = padic_roots([c, b, a], p, 2)
    print(roots_hensel)
