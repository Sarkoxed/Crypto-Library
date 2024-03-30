from sage.all import *


def HadamardRatio(v):
    return pow(abs(v.det()) / prod(vector(x).norm() for x in v), 1 / len(list(v)))


x = eval(input())
x = Matrix(x)
x = x.LLL(delta=3 / 4 + 0.001, eta=1 / 2 + 0.001)
print(x)
print(HadamardRatio(x))
