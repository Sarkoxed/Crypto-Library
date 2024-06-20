from LLL_improved import *

d = int(input())
print(d)
l = vector([int(input()) for i in range(d)])
m = identity_matrix(d - 1) * 2
m = m.insert_row(d - 1, vector([1] * (d - 1)))
m = m.T.insert_row(d - 1, l).T
m = [vector(x) for x in m]
print(m[-1])
print(HadamardRatio(m))
c = LLL_imporved(m)
for i in c:
    if all(x in [-1, 0, 1] for x in i):
        print(i)
print(HadamardRatio(c))
print(LLL_check(c))
