from Crypto.Util.number import getPrime, isPrime
from sage.all import GF, EllipticCurve, randint


def setup(nbit):
    p = getPrime(nbit - 1)
    q = 6 * p - 1
    while not (isPrime(q) and q % 3 == 2):
        p = getPrime(nbit - 1)
        q = 6 * p - 1

    return EllipticCurve(GF(q), [0, 1]), q


E, q = setup(128)
p = (q + 1) // 6
assert E.order() == 6 * p
P = E.gens()[0] * 6
assert P.order() == p

a, b, c = randint(1, p - 1), randint(0, p - 1), randint(0, p - 1)
A = a * P
B = b * P
C = c * P


def calc_shared(P, Q, s, l):
    G2 = GF(q**2)
    assert len(GF(q)(1).nth_root(3, all=True)) == 1
    w = G2(1).nth_root(3, all=True)[1]
    assert w != 1
    E1 = EllipticCurve(G2, [0, 1])

    Q = E1((Q[0] * w, Q[1]))
    return P.change_ring(G2).weil_pairing(Q, l) ** s


Ashared = calc_shared(B, C, a, p)
Bshared = calc_shared(A, C, b, p)
Cshared = calc_shared(A, B, c, p)

assert Ashared == Bshared
assert Ashared == Cshared
assert Ashared**p == 1
print(Ashared)
