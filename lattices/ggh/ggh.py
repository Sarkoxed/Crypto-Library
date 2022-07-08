from sage.all import *
from random import randint
from math import floor, ceil

def HadamardRatio(v):
    m = Matrix(v)
    prod = 1.0
    for i in range(len(v)):
        prod *= v[i].norm()
    return pow(abs(m.det()) / prod, 1/len(v))

def nearest(x):
    if(abs(floor(x) - x) < 0.5):
        return floor(x)
    return ceil(x)

def Babai_algorithm(base, vec):
    m = Matrix(base)
    sol = m.solve_left(vec)
    sol = vector([nearest(x) for x in sol])
    ans = zero_vector(len(base))
    for i in range(len(base)):
        ans += vector(base[i]) * sol[i]
    return ans

def get_sum_rows_m(i, j, a = 1, b = 1, dim=0):
    m = identity_matrix(dim)
    m[i, i] = a
    m[i, j] = b
    return m

def get_permutation_rows_m(i, j, dim):
    m = identity_matrix(dim)
    m[i,i] = 0
    m[j,j] = 0
    m[i, j] = 1
    m[j, i] = 1
    return m


def get_secret(dim: int, m):
    I = identity_matrix(dim)
    for i in range(100):
        m1 = get_sum_rows_m(randint(0, dim-1), randint(0, dim-1), 1, 1, dim)
        m2 = get_permutation_rows_m(randint(0, dim-1), randint(0, dim-1), dim)
        m = m1 * m2 * m 
    while(True):
        if(0 < HadamardRatio([vector(m.row(x)) for x in range(dim)]) < 0.01):
            return [vector(m.row(x)) for x in range(dim)]
        m1 = get_sum_rows_m(randint(0, dim-1), randint(0, dim-1), 1, 1, dim)
        m2 = get_permutation_rows_m(randint(0, dim-1), randint(0, dim-1), dim)
        m = m1 * m2 * m 
        


def keygen(dim: int, d: int):
    while True:
        vs = list()
        for i in range(dim):
            vi = list()
            for i in range(dim):
                vi.append(randint(-d, d))
            vi = vector(vi)
            vs.append(vi)
        if(HadamardRatio(vs) >= 0.90):
            break

    priv = vs
    pub = get_secret(dim, Matrix(priv))
    return (pub,  randint(0, 50)), priv

def encrypt(pub, binm, flag):
    base, sig = pub
    r  = vector([randint(-sig, sig) for i in range(len(base))])
    print(f"Random: {r}")
    if(flag):
        for i,j in zip(binm, base):
            r += i * j
        return r
    else:
        for i, j in zip(r, base):
            m += i * j
        return m

def decrypt(priv, pub, c):
    w = Matrix(priv)
    v = Babai_algorithm(priv, c)
    v1 = Babai_algorithm(pub[0], c) 
    print(f"Babai solved: {v}")
    print(f"Babai bad {v1}")
    print(f"R = {c - v}")
    m = Matrix(pub[0]).solve_left(v)
    m1 = Matrix(pub[0]).solve_left(v1)
    return m, m1

if __name__ == "__main__":
    #pub, priv = keygen(3, 100)
    #print(f"Pub: {pub}\nPriv: {priv}")
    #m = vector([1, 1, 1])
    #print(f"Message: {m}")
    #c = encrypt(pub, m, True)
    #print(f"Encrypted vector: {c}")
    #print(f"Decrypted vectors: {decrypt(priv, pub, c)}")
    priv = [vector([58, 53, -68]), vector([-110, -112, 35]), vector([-10, -119, 123])]
    pub = ([vector([324850, -1625176, 2734951]), vector([165782, -829409, 1395775]), vector([485054, -2426708, 4083804])], 30)
    print(priv, pub)
    print(HadamardRatio(priv))
    print(HadamardRatio(pub[0]))
    e = vector([8930810, -44681748, 75192665])
    print(f"Decrypted vectors: {decrypt(priv, pub, e)}")
    
