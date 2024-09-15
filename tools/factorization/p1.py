from sage.all import Zmod, var, PolynomialRing

def pp1(n):
    G = Zmod(n)
    s0, s1 = 2, G.random_element()

    x = var('x')
    P = PolynomialRing(Zmod(n), x)
    Q = P.quotient(P(x**2 - s1 * x + 1))

    beta = Q([0, 1])
    gamma = beta**n

    sn = beta**n + gamma**n


if __name__ == "__main__":
    pass
