import random
from Crypto.Util.number import isPrime, getPrime
from sage.all import Zmod, EllipticCurve, hilbert_class_polynomial, PolynomialRing, factor, randint, GF, var, ZZ, gcd
from division_polynomial import psi_odd_cached, init_cache_odd
import sys
# TODO hilbert poly impl

def extended_euclides(a,b,n):
    r0 = a; r1 = b
    s0 = 1; s1 = 0
    t0 = 0; t1 = 1

    while r1 != 0:
        tmp = int(list(r1)[-1])
        if gcd(tmp, n) != 1:
            print("Not invertible but factor found!")
            return gcd(tmp, n), False

        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
        t0, t1 = t1, t0 - q * t1
    
    if not r0.is_monic():
        hi = int(list(r0)[-1])
        if gcd(hi, n) != 1:
            print("Not invertible but factor found!")
            return gcd(hi, n), False

        r0 *= pow(hi, -1, n)
        s0 *= pow(hi, -1, n)
        t0 *= pow(hi, -1, n)
    
    return (r0, s0, t0), True

def inverse(a, mod, n):
    res, flag = extended_euclides(a, mod, n)
    if not flag:
        return res, False
    
    r, s, t = res
    assert (a * s) % mod == 1
    return s, True

def gcd_poly_zmod(a, b, n):
    res, flag = extended_euclides(a, b, n)
    if not flag:
        return res, False
    return res[0], True

# https://www.scitepress.org/Papers/2019/77866/77866.pdf
def factor4p1(n, D, B=10):
    sys.setrecursionlimit(2 * n.bit_length())
    
    H = hilbert_class_polynomial(-D) 
    x = var('x')

    Zm = Zmod(n)
    P = PolynomialRing(Zm, x)
    Q = P.quotient_ring(H)
    j = Q([0, 1])
    
    inv, flag = inverse(P(1728 - x), H,n)
    if not flag: # found not invertible element
        return inv

    inv = Q(inv)
    k = j * inv

    a, b = 3 * k, 2 * k
    
    for i in range(1, B + 10):
        xi = Q(randint(0, n))
        cache = init_cache_odd(a, b, xi)
        y_squared = xi**3 + a * xi + b

        z = P(psi_odd_cached(n, cache, y_squared).lift())
        d, flag = gcd_poly_zmod(z, P(H), n)
        if not flag:
            return d

        if d != 1:
            print("Don't know how to handle", d)


def get_complex_prime(nbit):
    D = 427
    while True:
        s = random.randrange(2 ** (nbit-1), 2 ** nbit)
        tmp = D * s ** 2 + 1
        if tmp % 4 == 0 and isPrime((tmp // 4)):
            return tmp // 4

if __name__ == "__main__":
    p = get_complex_prime(1020)
    q = getPrime(p.bit_length())
    #p = 86906341282696226881
    #q = 39331854789527579423
    n = p * q
     
    D = 427
    

    print(factor4p1(n, D))
    print(f"{p, q = }")
