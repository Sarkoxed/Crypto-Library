from sage.all import *
from Crypto.Util.number import getPrime, getRandomNBitInteger

x = var('x')

def get_ternary_poly(d1: int, d2: int, N: int):
    ans = [1] * d1 + [-1] * d2 + (N - d1 - d2) * [0]
    while True:
        shuffle(ans)
        return sum(x**i * ans[i] for i in range(N))

def center_lift(f, base):
    s = 0
    for n, i in enumerate(f):
        if(int(i) > base / 2):
            a = int(i) - base
        else:
            a = int(i)
        s += x**n * a
    return s

def keygen(nbit: int, nnbit: int):
    N = getPrime(nnbit)
    d = randint(0, N//2)
    p = getPrime(nbit)
    while True:
        q = random_prime((6 * d + 1) * p + 2**nbit)
        if(q > (6 * d + 1) * p):
            break

    assert gcd(N, p) == 1
    assert gcd(N, q) == 1
    assert gcd(p, q) == 1

    r = PolynomialRing(ZZ, x).quotient_ring(x**N - 1)
    r1 = PolynomialRing(GF(p), x).quotient_ring(x**N - 1)
    r2 = PolynomialRing(GF(q), x).quotient_ring(x**N - 1)
    print("start choosing polynomial f", N, d, p, q)
    while True:
        try:
            f = get_ternary_poly(d + 1, d, N)
            Fq = r2(f)**(-1)
            Fp = r1(f)**(-1)
            break
        except:
            continue
          
    g = get_ternary_poly(d, d, N)
    h = Fq * r2(g)
    return (N, p, q, d, h), (Fp, Fq, f, g)

def encrypt(pub, m):
    N, p, q, d, h = pub
    assert all(-p/2 < x[0] <= p/2 for x in m.coefficients())
    r = get_ternary_poly(d, d, N)

    r2 = PolynomialRing(GF(q), x).quotient_ring(x**N - 1)

    e = p * (h * r2(r)) + r2(m)
    return e

def decrypt(pri, pub, e):
    N, p, q, d, h = pub
    Fp, Fq, f, g = pri
    
    r1 = PolynomialRing(GF(p), x).quotient_ring(x**N - 1)
    r2 = PolynomialRing(GF(q), x).quotient_ring(x**N - 1)
    a = r2(f) * r2(e)
    a = center_lift(a, q)
    b = Fp * r1(a)
    return center_lift(b, p)

if __name__ == "__main__":
    pub, priv = keygen(10, 5)
    N, p, q, d, h = pub
    fp, fq, f, g = priv
    print(f"N = {N}, p = {p}, q = {q}, d = {d}, h = {h.lift()}")
    print(f"f = {f}\ng = {g}\nfp = {fp.lift()}\nfq = {fq.lift()}")
    m = sum(randint(-p//2+1, p//2)*x**i for i in range(N))
    print(f"MESSAGE: {m}")
    c = encrypt(pub, m)
    m = decrypt(priv, pub, m)
    print()
    print(f"ENCRYPTED: {c.lift()}")
    print()
    print(f"DECRYPTED: {m}")
    N, p, q = 7, 3, 37
