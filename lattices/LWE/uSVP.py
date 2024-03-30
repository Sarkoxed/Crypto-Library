from sage.all import Matrix, vector, GF, MatrixSpace, randint
from Crypto.Util.number import getPrime

# b = A * s + e

def uSVP(A, b, delta, q):
    m, n = A.dimensions() # m rows n columns
    L = Matrix(m + 1, n + 1)
    L.set_block(0, 0, A)
    L.set_block(0, n, Matrix(b).T)
    L[m, n] = delta
    
    L = L.T
    # L = [[A, b], [0, 1]]. (-s, 1) * L^T = (e, 1) - short
    print(L.LLL())
    for e in L.LLL():
        if abs(e[-1]) == 1 and all(abs(t) < delta for t in e):
            print(e)

q = getPrime(30)
m, n = 10, 20
delta = 10

A = MatrixSpace(GF(q), m, n).random_element()
print(A.rank())
s = vector(GF(q), [randint(0, q) for _ in range(n)])
e = vector(GF(q), [randint(-delta, delta) for _ in range(m)])

b = A * s + e

print(e)
print()
uSVP(A, b, delta, q)

# TODO make it work
