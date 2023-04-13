from sage.all import *


def normal(n, m):
    k = 1
    for i in range(m):
        k *= pow(2, n) - pow(2, i)
    return k


# n, m = int(input("n: ")), int(input("m: "))
n, m = 4, 4
ma = MatrixSpace(GF(2), nrows=m, ncols=n)
d, i = [], []
while True:
    g = ma.random_element()
    if g.rank() == m and g not in i:
        i.append(g)
    elif g.rank() != m and g not in d:
        d.append(g)
    if len(d) + len(i) == pow(2, m * n):
        break

print(normal(n, m) == len(i))
