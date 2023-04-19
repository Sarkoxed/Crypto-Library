from elliptic_curves import *
from weil_pairing import *


def MOV(P, Q, E, G, l: int):
    N = E.get_order(E((0, 1, 0)))
    assert l > floor(1 + sqrt(N))
    #### only for y^2 = x^3 + x
    k = 2
    print(N)
    E = EC(a4=1, K=GF((N - 1, 2)))
    while True:
        try:
            T = E.get_some_point()
            x, y = T._x, T._y
            assert x not in GF(N - 1) or y not in GF(N - 1)
        except:
            continue
        T1 = (N / l) * T # TODO maybe l**2
        if T1.is_infinity():
            continue
        a = Weil_pairing(P, T1, E, l)
        b = Weil_pairing(T1, P, E, l)
        n = discrete_log(b, a)
        assert Q == n * P
    return n


if __name__ == "__main__":
    g = GF(691)
    e = EC(a4=1, K=g)
    p = e((301, 14, 1))
    q = e((143, 27, 1))
    n = MOV(p, q, e, g, 173)
    print(n)
    print(p * n, e, q)
