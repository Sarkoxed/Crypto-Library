from sage.all import *
from random import randint
from math import floor, log, gcd

g = int(input("g-> "))
N = int(input("N-> "))
h = int(input("h-> "))
p = int(input("p-> "))


def getPowers(g, h, p, a, b, x):
    if x < p / 3:
        a += 1
    elif p / 3 <= x < 2 * p / 3:
        a *= 2
        b *= 2
    else:
        b += 1

    return a % (p - 1), b % (p - 1), (pow(g, a, p) * pow(h, b, p)) % p


ax, bx, ay, by = 0, 0, 0, 0
x, y = 1, 1
while True:
    ax, bx, x = getPowers(g, h, p, ax, bx, x)

    ay, by, y = getPowers(g, h, p, ay, by, y)
    ay, by, y = getPowers(g, h, p, ay, by, y)

    if (x - y) % p == 0:
        break

u = (ax - ay) % (p - 1)
v = -(bx - by) % (p - 1)
print(u, v, p - 1)

d = gcd(v, p - 1)

u //= d
w = (p - 1) // d
v //= d

ans = (pow(v, -1, w) * u) % w
fans = []
for k in range(0, d):
    fans.append(ans + k * w)

print(fans)
