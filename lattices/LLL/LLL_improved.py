from sage.all import *

from copy import copy

def HadamardRatio(v):
    m = Matrix(v)
    prod = 1.0
    for i in range(len(v)):
        prod *= v[i].norm()
    return pow(abs(m.det()) / prod, 1/len(v))

def nearest(x):
    if(abs(x - floor(x)) < 0.5):
        return floor(x)
    return ceil(x)

def LLL_imporved(base, delta=3/4):
    k, kmax = 1, 0
    orth = [base[0]] + [zero_vector(len(base)) for i in range(len(base) - 1)]
    mu = [[0 for i in range(len(base))] for j in range(len(base))]
    bs = [base[0].norm()**2] + [0 for i in range(len(base) - 1)]
    n = len(base)

    while(True):
        if(k > kmax):
            kmax = k
            orth[k] = base[k]
            
            for j in range(k):
                mu[k][j] = base[k].dot_product(orth[j]) / bs[j]
                orth[k] -= mu[k][j] * orth[j]
            print(Matrix(orth).T.n(23))
            print()
            bs[k] = orth[k].norm()**2

        while(True):
            reduce(k, k-1, mu, base)
            print("reduce")
            print(Matrix(base).T)
            print()
            if(bs[k] < (delta - mu[k][k-1]**2) * bs[k-1]):
                swap(k, kmax, mu, bs, base, orth)
                print('swap')
                print(Matrix(base).T)
                print()
                print(Matrix(orth).T.n(23))
                print()
                k = max(1, k-1)
                continue
            else:
                for l in range(k-2, -1, -1):
                    reduce(k, l, mu, base)
                k += 1
 
            if(k < n):
                break
            else:
                return base

def reduce(k, l, mu, base):
    if abs(mu[k][l]) <= 1/2: # i dunno, in algo its <= 1/2 but it doesn't equal sage LLL output(however it does better)
        return
    m = nearest(mu[k][l])
    base[k] -= m * base[l]
    mu[k][l] -= m
    for i in range(l - 1 + 1):
        mu[k][i] -= m * mu[l][i]
    return

def swap(k, kmax, mu, bs, base, orth):
    base[k], base[k-1] = base[k-1], base[k]

    for j in range(k - 2 + 1):
        mu[k][j], mu[k-1][j] = mu[k-1][j], mu[k][j]

    muu = mu[k][k-1]
    B = bs[k] + muu**2 * bs[k-1]
    mu[k][k-1] = muu * bs[k-1] / B

    a = orth[k] + muu * orth[k-1]
    b = orth[k-1] - mu[k][k-1] * a
    orth[k-1], orth[k] = a, b

    bs[k] = bs[k-1] * bs[k] / B
    bs[k-1] = B
    for i in range(k + 1, kmax+1):
        m = mu[i][k]
        mu[i][k] = mu[i][k-1] - muu * m
        mu[i][k-1] = m + mu[k][k-1] * mu[i][k]
    
    return

if __name__ == "__main__":
#    dim = 6
#    v1 = vector([20, 51, 35, 59 ,73, 73])
#    v2 = vector([14, 48, 33, 61, 47, 83])
#    v3 = vector([95, 41, 48, 84, 30, 45])
#    v4 = vector([0, 42, 74, 79, 20, 21])
#    v5 = vector([6, 41, 49, 11, 70, 67])
#    v6 = vector([23, 36, 6, 1, 46, 4])
#    base = [v1, v2, v3, v4, v5, v6]
#    dim = 3
#    v1 = vector([20, 16, 3])
#    v2 = vector([15, 0, 10])
#    v3 = vector([0, 18, 9])
#    base = [v1, v2, v3]


#base = [(0, 0, -2), (-1, -4, 4), (1, 1, -1)]
    base = eval(input())
    base = [vector(x) for x in base]
    print(base)
    print()
    c = LLL_imporved(base, 0.75)
    print(c)
    print(HadamardRatio(c))
