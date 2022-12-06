from sage.all import *
from random import randint
from math import floor, log, gcd


def getPowers(a, x, g, h, p, k):
    a, b = a

    if k > 1:
        N = k * p
        if x not in GF(p):
            par = sum(int(x) for x in list(x))
        else:
            par = int(x)
    else:
        N = p
        par = int(x)

    if par < N / 3:
        a += 1
    elif N / 3 <= par and par < 2 * N / 3:
        a *= 2
        b *= 2
    else:
        b += 1

    mod = p ** (k - 1) * (p - 1)
    return a % mod, b % mod, pow(g, a) * pow(h, b)


def pollard_rho(g, h, p, k=1):
    ax, bx, ay, by = 0, 0, 0, 0

    mod = p ** (k - 1) * (p - 1)

    x, y = 1, 1
    while True:
        ax, bx, x = getPowers((ax, bx), x, g, h, p, k)

        ay, by, y = getPowers((ay, by), y, g, h, p, k)
        ay, by, y = getPowers((ay, by), y, g, h, p, k)

        if x == y:
            break

    u = (ax - ay) % mod
    v = -(bx - by) % mod
#    print(u, v, mod)

    d = gcd(v, mod)
    print(d)

    u //= d
    w = mod // d
    v //= d

    ans = (pow(v, -1, w) * u) % w
    fans = []
    for k in range(0, d):
        fans.append(ans + k * w)

    return fans


#g = int(input("g-> "))
#h = int(input("h-> "))
#p = int(input("p-> "))
#k = int(input("k-> "))

p = random_prime(100000)
G = GF(p**2)
g = G.random_element()
x = randint(1, p-1)
h = g**x

print(f"p, g, h, x = {p}, {g}, {h}, {x}")

pos = pollard_rho(g, h, p, 2)
print(pos)
assert x in pos
