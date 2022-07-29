from sage.all import *
from copy import copy


def HadamardRatio(v):
    m = Matrix(v)
    prod = 1.0
    for i in range(len(v)):
        prod *= v[i].norm()
    return pow(abs(m.det()) / prod, 1 / len(v))


def nearest(x):
    if abs(x - floor(x)) < 0.5:
        return floor(x)
    return ceil(x)


def gram_shmi(base):
    for i in range(1, len(base)):
        vi = base[i]
        for j in range(i):
            mij = vi.dot_product(base[j]) / base[j].norm() ** 2
            vi -= mij * base[j]
        base[i] = vi
    return base


def LLL_own(base, delta=3 / 4):
    k = 1
    w = gram_shmi(copy(base))
    n = len(base)
    while k < n:
        mki = nearest(base[k].dot_product(w[k - 1]) / w[k - 1].norm() ** 2)
        base[k] -= base[k - 1] * mki

        mki = base[k].dot_product(w[k - 1]) / w[k - 1].norm() ** 2
        if w[k].norm() ** 2 >= (delta - mki**2) * w[k - 1].norm() ** 2:
            for i in range(k - 2, -1, -1):
                mki = nearest(base[k].dot_product(w[i]) / w[i].norm() ** 2)
                base[k] -= base[i] * mki

            k += 1
        else:
            base[k], base[k - 1] = base[k - 1], base[k]
            w = gram_shmi(copy(base))
            k = max(k - 1, 1)
    return base


if __name__ == "__main__":
    #    dim = 6
    #    v1 = vector([20, 51, 35, 59 ,73, 73])
    #    v2 = vector([14, 48, 33, 61, 47, 83])
    #    v3 = vector([95, 41, 48, 84, 30, 45])
    #    v4 = vector([0, 42, 74, 79, 20, 21])
    #    v5 = vector([6, 41, 49, 11, 70, 67])
    #    v6 = vector([23, 36, 6, 1, 46, 4])
    #    base = [v1, v2, v3, v4, v5, v6]
    #    print(base)
    #    print()
    #    c = LLL_own(base, 0.99)
    #    print(c)
    #    print(HadamardRatio(c))

    #    dim = 3
    #    v1 = vector([20, 16, 3])
    #    v2 = vector([15, 0, 10])
    #    v3 = vector([0, 18, 9])
    #    base = [v1, v2, v3]

    #   base = [(0, 0, -2), (-1, -4, 4), (1, 1, -1)]
    base = eval(input())
    base = [vector(x) for x in base]
    print(base)
    print()
    print(LLL_own(base))
    print(HadamardRatio(LLL_own(base)))
