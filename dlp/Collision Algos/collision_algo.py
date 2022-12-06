from sage.all import *
from random import randint
from math import floor, log


def babystep_giantstep(g, h, gf):
    n = g.multiplicative_order()
    n = 1 + floor(sqrt(int(n)))
    lg = [gf(1)]
    lh = [h]
    invg = g ** (-n)
    for i in range(1, n + 1):
        newg = lg[-1] * g
        newh = lh[-1] * invg

        if newg not in lg:
            lg.append(newg)
        if newh not in lh:
            lh.append(newh)

        if len(set(lh + lg)) < len(lh) + len(lg):
            for pg in lg:
                if pg in lh:
                    j = lh.index(ng)
                    return i + j * n


def babystep_giantstep_p(g, h, p):
    n = GF(p)(g).multiplicative_order()
    n = 1 + floor(sqrt(int(n)))
    lg = [1]
    lh = [h]
    invg = pow(g, -n, p)
    for i in range(1, n + 1):
        newg = (lg[-1] * g) % p
        newh = (lh[-1] * invg) % p

        if newg not in lg:
            lg.append(newg)
            lg.sort()
        if newh not in lh:
            lh.append(newh)
            lh.sort()

        # TODO implement bin search
        if len(set(lh + lg)) < len(lh) + len(lg):
            for pg in lg:
                if pg in lh:
                    j = lh.index(ng)
                    return i + j * n


def birthday_algo(p, g, h, N):
    n = floor(3 * sqrt(N))

    y = []
    z = []
    yi = []
    zi = []
    flag = True

    for i in range(n):
        a = randint(0, p)
        y.append(pow(g, a, p))
        yi.append(a)
        a = randint(0, p)
        z.append((pow(g, a, p) * h) % p)
        zi.append(a)

        for j in y:
            if j in z:
                y = yi[y.index(j)]
                z = zi[z.index(j)]
                flag = False
                break
        if not flag:
            break

    return (y - z) % (p - 1)


p = int(input("p-> "))
G = GF(p)
g = G(int(input("g-> ")))
# N = int(input("N-> "))
N = g.multiplicative_order()
h = G(int(input("h-> ")))

print(birthday_algo(p, g, h, N))
