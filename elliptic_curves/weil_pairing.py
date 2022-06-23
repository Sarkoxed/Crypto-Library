from elliptic_curves import *

#def g(P, Q, G):
#    var('x y')
#    xp, yp = [int(_) for _ in P.xy()]
#    xq, yq = [int(_) for _ in Q.xy()]
#    try:
#        if(P != Q):
#            l = int(G(yq - yp)/G(xp - xq))
#        else:
#            l = int(G(P.curve().a4() + 3 * xp**2)/ G(2 * yp))
#
#        return (y - yp - l * (x - xp))/(x + xp + xq - l**2)
#    except:
#        return x - xp
#
#
#def MillerAlgorithm(P, m: int, Base):
#    m = bin(m)[2:][::-1]
#    T, f = P, 1
#    n = len(m)
#    for i in range(n-2, -1, -1):
#        f = f*f* g(T, T, Base)
#        T += T
#        if m[i] == '1':
#            f = f*g(T, P, Base)
#            T += P
#    return f

def g_direct(P, Q, G, R):
    xp, yp = P._x, P._y
    xq, yq = Q._x, Q._y
    xr, yr = R._x, R._y

    try:
        if(P != Q):
            l = G(yq - yp)/G(xp - xq)
        else:
            l = G(P.curve().a4() + 3 * xp**2)/ G(2 * yp)

        return (yr - yp - l * (xr - xp))/(xr + xp + xq - l**2)
    except:
        return xr - xp


def MillerAlgorithm_direct(P, m: int, Base, Q):
    m = bin(m)[2:][::-1]
    T, f = P, 1
    n = len(m)
    for i in range(n-2, -1, -1):
        f = f*f* g_direct(T, T, Base, Q)
        T += T
        if m[i] == '1':
            f = f*g_direct(T, P, Base, Q)
            T += P
    return f

def Weil_pairing(P, Q, E, l: int):
    while True:
        S = E.get_some_point()
        if not (S * l).is_infinity():
            break

    fp = MillerAlgorithm_direct(P, 5, E._K, Q + S) / MillerAlgorithm_direct(P, 5, E._K, S)
    fq = MillerAlgorithm_direct(Q, 5, E._K, P - S) / MillerAlgorithm_direct(Q, 5, E._K, E((0,1,0))-S)
    return E._K(fp/fq)
    


if __name__ == "__main__":
    e = EC(a4=30, a6=34, K=GF(631))
    p = e((36, 60,1 ))
    q = e((121, 387, 1))
    s = e((0, 36, 1))
    fp = MillerAlgorithm_direct(p, 5, e._K, q + s) / MillerAlgorithm_direct(p, 5, e._K, s)
    fq = MillerAlgorithm_direct(q, 5, e._K, p - s) / MillerAlgorithm_direct(q, 5, e._K, e((0,1,0))-s)
    #x1, y1 = [int(_) for _ in (q + s).xy()]
    #x2, y2 = [int(_) for _ in s.xy()]
    #
    #x3, y3 = [int(_) for _ in (p - s).xy()]
    #x4, y4 = [int(_) for _ in (-s).xy()]
    #print(fp)
    #
    #print(fq)
    #
    #
    #first = G(fp(x=x1, y=y1)/fp(x=x2, y=y2))
    #second = G(fq(x=x3, y=y3)/fq(x=x4, y=y4))
    print(fp / fq)
