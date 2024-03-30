from sage.all import *
x = var('x')
def center_lift(g, ba):
    an = 0
    for i, j in enumerate(g):
        if(int(j) >= ba/2):
            z = int(j) - ba
        else:
            z = int(j)
        an += x**i * z
    return an

def get_polys(N, p, q):
    Q = PolynomialRing(GF(q), x).quotient_ring(x**N - 1)
    P = PolynomialRing(GF(p), x).quotient_ring(x**N-1)
    sp = center_lift(P.random_element(), p)
    tp = center_lift(P.random_element(), p)
    R = PolynomialRing(ZZ, x).quotient_ring(x**N - 1)
    while True:
        try:
            F = sum([x**i * j for i, j in enumerate([randint(-1, 1) for k in range(N)])])
            f = p * F
            g = sum([x**i * j for i, j in enumerate([randint(-p//2, p//2) for k in range(N)])])
            A = floor(q/(2*p) - 1/2)
            B = ceil(p**2 * N / 4)
            r = sum([x**i * j for i, j in enumerate([randint(-A, A) for k in range(N)])])
            s0 = sp + p * r
            h = Q(f)**(-1) * Q(g)
            t0 = center_lift(h * Q(s0), q)
            a = center_lift(P(g)**(-1) * P(tp - t0), p)
            s = R(s0 + a * f)
            t = R(t0 + a * g)
            return (s, t, sp, tp, F, f, g, A, B, r, h, a, P, Q, t0)
        except AssertionError:
            print("Fuck")
        except Exception as e:
            continue

#N, p, q = 19, 13, 23
N, p, q = 7, 3, 23
mr = 0
for i in range(100000):
    s, t, sp, tp, F, f, g, A, B, r, h, a, P, Q, t0 = get_polys(7, 3, 23)
#    print(max([abs(x) for x in s.lift().coefficients()]), (q/2 + B))
#    print(f"sp = {tp}")
#    print(f"r = {r}")
#    print(f"a = {a}")
#    print(f"f = {f}")
#    print(f"a*f = {expand(a*f)}")
#    print(f"A = {A}, B = {B}")
#    print(f"t = {t}")
#    print(f"t0 = {t0}")
#    print(f"P(t) = {P(t).lift()}")
#    print(f"tp = {tp}")
#    print(f"P(tp) = {P(tp).lift()}")
#    print()
    sss = max([abs(x) for x in s.lift().coefficients()])
    if(sss > mr):
        mr = sss
    #try:
    #    assert max([abs(x) for x in s.lift().coefficients()]) < 40
    #    assert P(s) == P(sp)
    #    assert P(t) == P(tp)
    #    assert Q(t) == Q(h * s)
    #    #if(len(a.coefficients()) == N):
    #    #    print(a, f)
    #except:
    #    print(max([abs(x) for x in s.lift().coefficients()]))
    #    print(f"sp = {sp}\ntp = {tp}\nF = {F}\ng = {g}\nf = {f}\na = {a}\nh = {h}\ns = {s}\na*f = {PolynomialRing(ZZ, x).quotient_ring(x**N - 1)(a*f)}")
    #    break

 #   if(not all(abs(x) < q/2 + B for x, y in s.coefficients())):
 #       print(s,t, sp, tp, F, f, g, A, B, r, h)
    if(i % 100 == 0):
        print(mr, i)
print(mr)
