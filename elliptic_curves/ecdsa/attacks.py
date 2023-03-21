from ecdsa import hash, sign, verify, keygen
from random import Random
from testparams import p, q, a, b


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
    m: int = 0
    a: int = 0
    b: int = 0
    s: int = 0

    def __init__(self, m, aas, s):
        self.m = m
        self.aas = aas
        self.b = b
        self.s = s

    def next(self):
        tmp = sum(x * y for x, y in zip(self.aas, self.s)) % self.m
        self.s = self.s[1:]
        self.s.append(tmp)
        yield tmp


def recurrence_gen_based(pk, sk, ms, ass, s, N):
    sigs = [sign(m, pk, sk, lcg) for m in ms]

    return None


def truly_random_gen_based(pk, sk, ms, N):
    return None


if __name__ == "__main__":
    pk, sk = keygen(p, a, b, q)

    res = repeated_nonce(pk, sk, b'aboba', b'kickapoo')
    print(res)
