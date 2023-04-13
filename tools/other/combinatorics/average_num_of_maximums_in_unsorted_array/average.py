from sage.all import gamma, var, factorial, N, euler_gamma, psi
from get_cycles import req 
from random import shuffle
from gmpy2 import mpfr


def asymp(k, n=10_000):
    l = list(range(k))
    d = dict()
    for _ in range(n):
        shuffle(l)
        tmp = 1
        max = l[0]
        for m in l[1:]:
            if(m > max):
                max = m
                tmp += 1
        try:
            d[tmp] += 1
        except:
            d[tmp] = 1
    return mpfr(sum(d[i] * i for i in d.keys()))/mpfr(n)

def direct(n):
    return mpfr(sum(req(n, k) * k for k in range(1, n+1))) / mpfr(factorial(n))

def very_direct(m):
#    var('n, x')
#    f = gamma(x + n) / (gamma(x)* gamma(n+1))
#    g = f.derivative(x)
#    return mpfr(g(x=1, m=n + 0.0001))
    return euler_gamma.n() + psi(m+1).n()

from time import time
def timing(func, par):
    x = time()
    t = func(par)
    print(t)
    y = time()
    print(f"time: {y-x}")

#for k in range(1, 20):
#    print(k)
#    for _ in [asymp, direct, very_direct]:
#        timing(_, k)
#    print("_"*50)

#obviously very_direct is the fastest one

