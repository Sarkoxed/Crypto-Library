# https://datatracker.ietf.org/doc/html/rfc9380#name-shallue-van-de-woestijne-me

from sage.all import EllipticCurve, GF, random_prime
from hashlib import sha3_512
from random import randrange, seed


def hash_to_field(m: bytes, p: int):
    _m = sha3_512(m).digest()
    x = int.from_bytes(_m[:32], "big") % p
    y = int.from_bytes(_m[32:], "big") % p
    return x, y


def find_Z(A, B, p):
    seed(25519)
    G = GF(p)
    while True:
        Z = G(randrange(0, p))

        gZ = Z**3 + A * Z + B
        if gZ == 0:
            continue

        T = -(3 * Z**2 + 4 * A) / (4 * gZ)
        if T == 0:
            continue

        if not T.is_square():
            continue

        Z1 = -Z / 2
        gZ1 = Z1**3 + A * Z1 + B

        if gZ.is_square() or gZ1.is_square():
            return Z


def sgn0(x):
    return int(x) % 2


def map_to_point(u, A, B, p):
    G = GF(p)
    Z = find_Z(A, B, p)

    u = G(u)
    gZ = Z**3 + A * Z + B

    tv1 = u * u * gZ
    tv2 = 1 + tv1
    tv1 = 1 - tv1

    tv3 = pow(tv1 * tv2, -1)
    tv4 = (-gZ * (3 * Z**2 + 4 * A)).sqrt()

    if sgn0(tv4):
        tv4 = -tv4

    tv5 = u * tv1 * tv3 * tv4
    tv6 = -4 * gZ / (3 * Z**2 + 4 * A)

    x1 = -Z / 2 - tv5
    x2 = -Z / 2 + tv5
    x3 = Z + tv6 * (tv2**2 * tv3) ** 2

    gx1 = x1**3 + A * x1 + B
    gx2 = x2**3 + A * x2 + B
    gx3 = x3**3 + A * x3 + B
    x, y = 0, 0
    if gx1.is_square():
        x, y = (x1, gx1.sqrt())
    elif gx2.is_square():
        x, y = (x2, gx2.sqrt())
    else:
        assert gx3.is_square()
        x, y = (x3, gx3.sqrt())

    if sgn0(y) != sgn0(u):
        y = -y
    assert sgn0(y) == sgn0(u)

    return (x, y)


def hash_to_point(m, A, B, p):
    e0, e1 = hash_to_field(m, p)
    p0 = map_to_point(e0, A, B, p)
    p1 = map_to_point(e1, A, B, p)

    E = EllipticCurve(GF(p), [A, B])
    P0 = E(p0)
    P1 = E(p1)
    return P0 + P1


p = 0x2523648240000001BA344D80000000086121000000000013A700000000000013
K = GF(p)
a = K(0x0000000000000000000000000000000000000000000000000000000000000000)
b = K(0x0000000000000000000000000000000000000000000000000000000000000002)
E = EllipticCurve(K, (a, b))
G = E(
    0x2523648240000001BA344D80000000086121000000000013A700000000000012,
    0x0000000000000000000000000000000000000000000000000000000000000001,
)
E.set_order(0x2523648240000001BA344D8000000007FF9F800000000010A10000000000000D * 0x01)

m = b"aboba"
H = hash_to_point(m, a, b, p)
print(H)
