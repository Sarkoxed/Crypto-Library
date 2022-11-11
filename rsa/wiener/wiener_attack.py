from gmpy2 import mpq
from Crypto.Util.number import getPrime
from math import floor, gcd
from random import randint
from sage.all import *

def get_frac(a, b):
    frac = []
    while a * b:
        c = a//b
        frac.append(c)
        a %= b        
        b, a = a, b
    return frac

def get_partial_frac(r, n):
    x = mpq(r[n]) + mpq(1,r[n+1])
    for i in range(n-1, -1, -1):
        x = mpq(r[i]) + mpq(1)/x
    return x

def wiener(e, n):
    r = get_frac(e, n)
    for i in range(len(r)-1):
        an = get_partial_frac(r, i)
        k, d = int(an.numerator), int(an.denominator)
        if d % 2 == 1 and (d * e - 1) % k == 0:
            su = n + 1 - (d * e - 1) // k
            pr = n
            var('x')
            s = x**2 - su * x + pr
            roots = s.roots()
            if roots[0][0].is_integer():
                p = roots[0][0]
                q = n / p
                return p, q

def gen_params(nbit):
    p, q = getPrime(nbit), getPrime(nbit)
    n = p * q
    b = floor(1/3 * pow(n, 1/4))
    while True:
        d = randint(0, b)
        if gcd(d, (p-1)*(q-1)) != 1:
            continue
        e = pow(d, -1, (p-1)*(q-1))
        return e, n

e, n = gen_params(512)
print(wiener(e, n))
