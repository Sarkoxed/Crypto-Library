#https://math.stackexchange.com/questions/1863037/discrete-logarithm-modulo-powers-of-a-small-prime
from sage.all import GF, discrete_log, gcd, crt

def tetta(k, p, s):
    tmp_mod = pow(p, 2 * s - 1)
    tmp_phi = pow(p, 2 * s - 2) * (p - 1)

    exp1 = pow(p, s-1, tmp_phi)
    exp1 = ((p-1) * exp1) % tmp_phi

    numerator = pow(k, exp1, tmp_mod) - 1
    assert numerator % p**s == 0

    res = (numerator // pow(p, s)) % pow(p, s-1)
    return res

def dl(g, h, p, s, x=None):
    if x is None:
        if p < 2**40:
            G = GF(p)
            x = discrete_log(G(h), G(g))
        else:
            # try something else...
            return None
    tg = tetta(g, p, s)
    th = tetta(h, p, s)
    mod = p**(s-1)
    d1 = gcd(tg, th)
    d2 = gcd([d1, mod])
    if d1 == d2:
        tg //= d1
        th //= d1
        mod //= d1
    else:
        return None # no solution for ya

    d3 = gcd([tg, mod])
    if d3 != 1:
        return None

    res = (pow(tg, -1, mod) * th) % mod

    reses = []
    for k in range(d1):
        cur = res + k * mod
        try:
            cur = crt([cur, x], [pow(p, s-1), p-1])
            if pow(g, cur, p**s) == h:
                reses.append(cur)
        except ValueError:
            continue
    return reses

g = 542647450400054587231595
h = 403807253274655505719706
p = 101
n = 12
print(dl(g, h, p, n))
