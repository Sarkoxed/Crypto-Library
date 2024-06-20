from sage.all import *
from ntru import center_lift

x = var("x")


def getMatrix(h, q, N):
    m = identity_matrix(N)
    for i in range(N):
        m = m.insert_row(i + N, zero_vector(N))
    h1 = Matrix(h)
    for i in range(1, N):
        h1 = h1.insert_row(i, vector(h[N - i :] + h[: N - i]))
    for i in range(N):
        v = zero_vector(N)
        v[i] = q
        h1 = h1.insert_row(N + i, v)
    m = m.T
    for i, j in enumerate(h1.columns()):
        m = m.insert_row(i + N, j)
    return m.T


def getPolys(v, N):
    f, g = 0, 0
    for i in range(N):
        f += x**i * v[i]
        g += x**i * v[N + i]
    return f, g


if __name__ == "__main__":
    h = (39, 9, 33, 52, 58, 11, 38, 6, 1, 48, 41)
    N, q, p = 11, 67, 3
    m = getMatrix(h, q, N)
    Q = PolynomialRing(GF(q), x).quotient_ring(x**N - 1)
    P = PolynomialRing(GF(p), x).quotient_ring(x**N - 1)
    v = m.LLL(delta=0.75, eta=0.5)[0]
    f, g = getPolys(v, N)
    h = sum(x**i * h[i] for i in range(N))
    while True:
        if Q(h) * Q(f) == Q(g):
            break
        f, g = x * f, x * g
    e = (52, 50, 50, 61, 61, 7, 53, 46, 24, 17, 50)
    e = sum(x**i * e[i] for i in range(N))

    a = center_lift(Q(f) * Q(e), q)
    b = P(f) ** (-1) * P(a)
    print(center_lift(b, p))
