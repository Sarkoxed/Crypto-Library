from sage.all import EllipticCurve, GF, is_prime
from Crypto.Util.number import getPrime
from random import randint
from hashlib import shake_256


def keygen(p: int, a: int, b: int, q: int, G = None):
    e = EllipticCurve(GF(p), [a, b])
    o = e.order()
    assert o % q == 0
    assert is_prime(q)

    if G is None:
        while True:
            g = e.random_element()
            G = g * (o // q)
            if not G.is_zero():
                break
    else:
        G = e(G)

    d = randint(1, q-1)
    Q = d * G
    return (G, Q, q), d


def hash(m: bytes, n: int):
    e = int.from_bytes(shake_256(m).digest(n), 'big')
    return e


def sign(m: bytes, pk, sk):
    G, Q, q = pk
    d = sk
    e = hash(m, int(q).bit_length() // 8)

    k = randint(1, q-1) # try to create k from m and d
    R = k * G
    r = int(R.xy()[0]) % q
    assert r != 0

    s = (pow(k, -1, q) * (e + r * d)) % q
    assert s != 0

    return (r, s)


def verify(sig, pk, m):
    G, Q, q = pk
    r, s = sig
    assert not Q.is_zero()
    # check that Q in E
    assert (q * Q).is_zero()
    assert 1 <= r <= q - 1
    assert 1 <= s <= q - 1
    e = hash(m, int(q).bit_length() // 8)
    
    inv = pow(s, -1, q)
    u1 = (e * inv) % q
    u2 = (r * inv) % q
    R = u1 * G + u2 * Q
    assert not R.is_zero()
    return r == int(R.xy()[0]) % q


if __name__ == "__main__":
    p = 23894735687533695465072949951707623720448341596203786833271594243268666934921
    q = 4709088060659619911309156036222252492080017328896608184431
    a, b = 1, 3

    pk, sk = keygen(p, a, b, q)
    m = b"abobafinder"

    sig = sign(m, pk, sk)
    print(verify(sig, pk, m))
