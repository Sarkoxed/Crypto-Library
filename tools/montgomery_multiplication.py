from random import randrange

q = 0x30644E72E131A029B85045B68181585D2833E84879B9709143E1F593F0000001


class montgomery:
    modulus: int = 0
    mf: int = 0
    k: int = 256
    R: int = 0
    mod_inv: int = 0
    R_inv: int = 0

    def __init__(self, a: int = -1, N: int = q):
        self.modulus = N
        self.R = pow(2, self.k)
        self.mod_inv = pow(-self.modulus, -1, self.R)

        self.mf = (a * self.R) % self.modulus

    def copy(self):
        res = montgomery(N=self.modulus)
        res.mf = self.mf
        return res

    def __add__(self, other):
        if self.modulus != other.modulus or self.R != other.R:
            raise ValueError("Operand mismatch")

        res = self.copy()
        res.mf = self.mf + other.mf
        res.mf = res.mf - self.modulus if res.mf >= self.modulus else res.mf
        return res

    def __neg__(self):
        res = self.copy()
        res.mf = res.modulus - res.mf
        return res

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if self.modulus != other.modulus or self.R != other.R:
            raise ValueError("Operand mismatch")

        tmp_res = self.copy()
        mf_res = self.reduce(self.mf * other.mf)  # N^2 < N * R
        tmp_res.mf = mf_res
        return tmp_res

    def reduce(self, T=None):
        if T is None:
            T = self.mf

        m = ((T & (self.R - 1)) * self.mod_inv) & (self.R - 1)
        t = (T + self.modulus * m) >> self.k
        if t >= self.modulus:
            t -= self.modulus
        return t

    def __repr__(self):
        return str(self.reduce())


def test(n=1_000_000):
    from tqdm import tqdm

    for _ in tqdm(range(n)):
        t1 = randrange(0, q)
        t2 = randrange(0, q)
        a = montgomery(t1)
        b = montgomery(t2)
        c = a + b
        d = a * b
        assert a.reduce() == t1
        assert b.reduce() == t2
        assert c.reduce() == (t1 + t2) % q
        assert d.reduce() == (t1 * t2) % q


def timing(n=1_000_000):
    from tqdm import tqdm
    from time import time

    mont_t = 0.0
    ord_t = 0.0
    cc_t = 0.0
    init_t = 0.0
    for _ in tqdm(range(n)):
        start = time() 
        t1 = randrange(0, q)
        t2 = randrange(0, q)
        a = montgomery(t1)
        b = montgomery(t2)
        end = time()
        init_t += end - start

        start = time()
        r1 = a * b
        end = time()
        mont_t += end - start

        start = time()
        r2 = (t1 * t2) % q
        end = time()
        ord_t += end - start
        
        start = time()
        assert r1.reduce() == r2
        end = time()
        cc_t += end - start

    print(f"Overall montgomery: {mont_t}")
    print(f"Overall ordinary: {ord_t}")
    print(f"Aftermath: {cc_t}")
    print(f"Init: {init_t}")



timing()
