from sage.all import *

n, m = 7, 2
ma = MatrixSpace(GF(2), nrows=m, ncols=n)
a = []
while len(a) != pow(2, m * n):
    g = ma.random_element()
    if g not in a:
        a.append(g)

n1 = 0
a = [[[1 if int(z) else -1 for z in x] for x in y] for y in a]
for el in a:
    f = [[el[i][j] for i in range(len(el))] for j in range(len(el[0]))]
    # print(el)
    # print()
    # print(f)
    # print("----------------------------------------")
    if all(product(x) == 1 for x in el) and all(product(x) == 1 for x in f):
        n1 += 1


print(n1 == pow(2, (n - 1) * (m - 1)))
