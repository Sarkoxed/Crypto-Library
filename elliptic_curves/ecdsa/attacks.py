from random import Random

from Crypto.Util.number import long_to_bytes
from sage.all import (GF, EllipticCurve, Matrix, PolynomialRing, gcd, var, vector)

from ecdsa import hash, keygen, sign, verify
from testparams import a, b, p, q


def repeated_nonce(pk, sk, m1, m2):
    G, Q, q = pk
    R = Random()
    seed = 0x1337

    R.seed(seed)
    sig1 = sign(m1, pk, sk, R.randint)
    r1, s1 = sig1

    R.seed(seed)
    sig2 = sign(m2, pk, sk, R.randint)
    r2, s2 = sig2

    assert r1 == r2

    st = int(s1 - s2) % q
    e1 = hash(m1, q.bit_length() // 8)
    e2 = hash(m2, q.bit_length() // 8)
    et = (e1 - e2) % q
    st = (st * pow(et, -1, q)) % q
    k = pow(st, -1, q)
    d = ((s1 * k - e1) * pow(r1, -1, q)) % q

    return d == sk


def lattice_based(pk, sk, ms):
    return None


class recg:
    def __init__(self, m, cfs, s):
        self.m = m
        self.cfs = cfs
        self.s = s

    def next(self, a, b):
        tmp = sum(x * self.s**i for i, x in enumerate(self.cfs)) % self.m
        self.s = tmp
        return tmp


def recurrence_gen_based(
    pk, sk, ms, n, flag=True
):  # linear recurrence mod q? TODO arbitrary lcg modulus
    x = var("x")
    G, Q, q = pk
    d = sk
    B = [Random().randint(0, q) for _ in range(n + 1)]

    rs, ss, ks = [], [], []
    m = long_to_bytes(ms[0])
    sig, k = sign(m, pk, sk, Random().randint, True)
    ms[0] = hash(m, q.bit_length()//8)
    ks.append(k)
    rs.append(sig[0])
    ss.append(sig[1])

    global R
    R = recg(q, B, k)

    if flag:
        m = n + 4  # easier root finder
    else:
        m = n + 3

    for i in range(1, m):
        m = long_to_bytes(ms[i])
        sig = sign(m, pk, sk, R.next)
        ms[i] = hash(m, q.bit_length()//8)
        rs.append(sig[0])
        ss.append(sig[1])

    # attack
    P = PolynomialRing(GF(q), x)
    kx = []
    for m, r, s in zip(ms, rs, ss):
        inv = pow(s, -1, q)
        kx.append(P((m + r * x) * inv))

    M = []
    for i in range(n + 1):
        tmp = [kx[i] ** j for j in range(n + 1)]
        M.append(tmp)
    M = Matrix(P, M)

    res = vector(P, kx[1 : n + 2])
    bx = M.solve_right(res)
    gc = gcd(
        bx[0].denominator(), bx[1].denominator()
    )  # check if det is easier or algo from paper

    if flag:
        k1 = kx[-3]
        k2 = kx[-2]
        k3 = kx[-1]
        final_poly_1 = P(
            sum(b * gc * k1**j for j, b in zip(range(n + 1), bx)) - k2 * gc
        )
        final_poly_2 = P(
            sum(b * gc * k2**j for j, b in zip(range(n + 1), bx)) - k3 * gc
        )
        res = gcd(final_poly_1, final_poly_2)

        da = res.roots()[0][0]
        return d == da
    else:
        k1 = kx[-2]
        k2 = kx[-1]
        final_poly = P(sum(b * gc * k1**j for j, b in zip(range(n + 1), bx)) - k2 * gc)
        ds = [r[0] for r in final_poly.roots()]
        return d in ds


class lcg:
    def __init__(self, m, cfs, st):
        self.m = m
        self.cfs = cfs
        self.st = st

    def next(self, a, b):
        tmp = sum(s * c for s, c in zip(self.st, self.cfs)) % self.m
        self.st = self.st[1:]
        self.st.append(tmp)
        return tmp


def linear_congr(
    pk, sk, ms, n, flag=True
):  # linear recurrence mod q? TODO arbitrary lcg modulus
    x = var("x")
    G, Q, q = pk
    d = sk
    B = [Random().randint(0, q) for _ in range(n)]

    rs, ss, ks = [], [], []
    for i in range(n):
        m = long_to_bytes(ms[i])
        sig, k = sign(m, pk, sk, Random().randint, True)
        ms[i] = hash(m, q.bit_length() // 8)
        ks.append(k)
        rs.append(sig[0])
        ss.append(sig[1])

    global R
    R = lcg(q, B, ks)

    if flag:
        m = 2 * n + 2  # easier root finder
    else:
        m = 2 * n + 1

    for i in range(n, m):
        m = long_to_bytes(ms[i])
        sig = sign(m, pk, sk, R.next)
        ms[i] = hash(m, q.bit_length() // 8)
        rs.append(sig[0])
        ss.append(sig[1])

    # attack
    P = PolynomialRing(GF(q), x)
    kx = []
    for m, r, s in zip(ms, rs, ss):
        inv = pow(s, -1, q)
        kx.append(P((m + r * x) * inv))

    M = []
    for i in range(n):
        tmp = kx[i : i + n]
        M.append(tmp)
    M = Matrix(P, M)

    res = vector(P, kx[n : 2 * n])
    bx = M.solve_right(res)
    gc = gcd(bx[0].denominator(), bx[1].denominator())

    if flag:
        final_poly_1 = P(
            sum(b * gc * k for k, b in zip(kx[-n - 2 : -2], bx)) - kx[-2] * gc
        )
        final_poly_2 = P(
            sum(b * gc * k for k, b in zip(kx[-n - 1 : -1], bx)) - kx[-1] * gc
        )
        res = gcd(final_poly_1, final_poly_2)
        da = res.roots()[0][0]
        return d == da
    else:
        final_poly = P(
            sum(b * gc * k for k, b in zip(kx[-n - 1 : -1], bx)) - kx[-1] * gc
        )
        ds = [r[0] for r in final_poly.roots()]
        return d in ds


def truly_random_gen_based(pk, sk, ms, N):
    return None

import time
def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap

if __name__ == "__main__":
    pk, sk = keygen(p, a, b, q)

    print("Repeated nonce attack: ")
    print(timing(repeated_nonce)(pk, sk, b'aboba', b'kickapoo'))
    print()

    n = 40

    print("Linear relation 2n + 1:")
    m = 2 * n + 1
    ms = [Random().randint(0, q) for _ in range(m)]
    print(timing(linear_congr)(pk, sk, ms, n, False))
    print()

    print("Linear relation 2n + 2 gcd:")
    m = 2 * n + 2
    ms = [Random().randint(0, q) for _ in range(m)]
    print(timing(linear_congr)(pk, sk, ms, n, True))
    print()

    print("Polynomial congruence n + 3:")
    m = n + 3
    ms = [Random().randint(0, q) for _ in range(m)]
    print(timing(recurrence_gen_based)(pk, sk, ms, n, False))
    print()

    print("Polynomial congruence n + 4 gcd:")
    m = n + 4
    ms = [Random().randint(0, q) for _ in range(m)]
    print(timing(recurrence_gen_based)(pk, sk, ms, n, True))
    print()
