from sage.all import *
from random import randint
from math import floor, log

g = int(input("g-> "))
N = int(input("N-> "))
h = int(input("h-> "))
p = int(input("p-> "))

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

print((y - z) % (p - 1))
