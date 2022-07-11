from sage.all import *
from copy import copy
from time import time

def GaussianExpected(base):
    a = pow(gamma(1 + len(base)/2) * abs(Matrix(base).det()), 1/len(base)) / sqrt(pi)
    b = sqrt(len(base)/(2 * pi * e)) * pow(abs(Matrix(base).det()), 1/ len(base))
    return a, b

def LLL_check(base, delta=3/4, eta=1/2):
    w = [vector(x) for x in Matrix(base).gram_schmidt()[0]]
    mu = [[base[i].dot_product(w[j]) / w[j].norm()**2 for j in range(len(base))] for i in range(len(base))]
#    print(mu)
    for i in range(len(mu)):
        for j in range(len(mu)):
            if(not(i == j or abs(mu[i][j]) <= eta)):
                return False
    for i in range(1, len(base)):
        if(not(w[i].norm()**2 >= (delta - mu[i][i-1]**2) * w[i-1].norm()**2)):
            return False
    return True

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
#            print(Matrix(orth).T.n(23))
#            print()
            bs[k] = orth[k].norm()**2

        while(True):
            reduce(k, k-1, mu, base)
#            print("reduce")
#            print(Matrix(base).T)
#            print()
            if(bs[k] < (delta - mu[k][k-1]**2) * bs[k-1]):
                swap(k, kmax, mu, bs, base, orth)
#                print('swap')
#                print(Matrix(base).T)
#                print()
#                print(Matrix(orth).T.n(23))
#                print()
                k = max(1, k-1)
                continue
            else:
                for l in range(k-2, -1, -1):
                    reduce(k, l, mu, base)
     #           print(HadamardRatio(base))
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
#    N, q = int(input()), int(input())
#     base = [vector([int(pow(i+1 + N, j+1, q)) for j in range(N)]) for i in range(N)]
    N = int(input())
    base = [vector([int(x) for x in input().split()]) for i in range(N)]
    c = base[0].norm() 
    k = 0
    v = base[0]
    for i in range(N):
        if(base[i].norm() < c):
            c = base[i].norm()
            k = i
            v = base[i]
    print("Base shortest vector: ", v)
    print("Base shortest length: ", c.n())

    print()
    for i in base:
        for j in i:
            print(j, end=" ")
    print()
    print(Matrix(base).T)
    print()
    l0, l1 = GaussianExpected(base)
    print("Base Hadamard Ratio: ", HadamardRatio(base))

    beg = time()
    base = LLL_imporved(copy(base), delta=0.99)
    end = time()
    print("Time Elapsed: ", beg - end)
    print()
    print(Matrix(base).T)
    print()
    print("LLL reduced Hadamard Ratio: ", HadamardRatio(base))

    print("The expected shortest length: ", l0.n())
    print("Approximately shortest length: ", l1.n())
    c = base[0].norm() 
    k = 0
    v = base[0]
    for i in range(N):
        if(base[i].norm() < c):
            c = base[i].norm()
            k = i
            v = base[i]
    print("LLL reduced shortest vector: ", v)
    print("LLL reduced shortest length: ", c.n())
    print("It's number: ", k + 1)
    print(LLL_check(base, delta=0.99))

