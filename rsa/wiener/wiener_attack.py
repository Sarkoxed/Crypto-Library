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

#e, n = gen_params(512)
#print(wiener(e, n))

c = 146609209560709008867501625511012963798366446188884940594883580035081181357908350444066288274737075484194675981734840043175841220110589624839945404259933280542136270877842189449531075021117124079772783962011903474213066730283039401718509518393042139396828524597532154130638454544547313312056721197430725959299
n = 162007462693058351745831681315104298306073962511966578579313284406600351073111162480878481296570735333509906113306883609229329701248918329557062430852130211519420303365980593177289016734225154121905475270227704665812501879471997575784021212438943542517898424098134538591479360819622357477436348356184676004413
e = 117672143050718886427591737399661180828627077276876162679592763848253504307219396011638882870429835716400484471453290104315646923704945455598750108082809727586968945176404775523924145520715504179233178433732760509106021510353879158813592024293184085678034617462737215011108254348252644877234447080586151974521
p, q = wiener(e, n)

d = pow(e, -1, (int(p)-1)*(int(q)-1))

m = pow(int(c), int(d), int(n))
from Crypto.Util.number import long_to_bytes
print(long_to_bytes(m))
