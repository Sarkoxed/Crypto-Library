from sage.all import (
    EllipticCurve,
    GF,
    random_prime,
    randint,
    var,
    binomial,
    PolynomialRing,
    gcd,
)

# if a = 0, N > 0, there exists P \in E(F_q): ord(P) = N => E[N] \in E(F_q^2)
# if p = 2(mod 3) => cyclic


def rebase(n, b):
    if n < b:
        return [n]
    else:
        return [n % b] + rebase(n // b, b)


# E(F_q)
def is_supersingular(E, p):
    return E.order() % p == 1


# E(F_p) for p >= 5, a = 0, E.order() == p + 1
# y^2 = x^3 + b - supersingular <= q % 3 == 2
def fast_multiplication(P, k, q):
    e = P.curve()
    points_map = dict()
    res = P * 0

    for i, ki in enumerate(rebase(k, q)):
        Pi, power = points_map.setdefault(ki, (P * ki, 0))
        pix, piy = Pi.xy()

        for j in range(i - power):
            pix = pix**q
            piy = piy**q
            pix = pix**q
            piy = -(piy**q)

        Piqi = e((pix, piy))
        points_map[ki] = (Piqi, i)
        res += Piqi
    return res


def Hp(T, p):
    return sum(binomial((p - 1) // 2, i) ** 2 * T**i for i in range((p - 1) // 2 + 1))


# legendre form: y^2 = x * (x - 1) * (x - lambda)
# y^2 = (x - e1) * (x - e2) * (x - e3), x1 <- (e2 - e1)^(-1) * (x - e1), y1 <- (e2-e1)^(-3/2) * y, lambda = (e3 - e1) / (e2 - e1)
def is_supersingular_legendre(A, B, p):
    x = var("x")
    for i in range(1, 3 + 1):
        P = PolynomialRing(GF(p**i), x)
        Q = P.quotient(x**3 + A * x + B)

        tmp = Q(x)
        for _ in range(i):
            tmp **= p

        if tmp - Q(x) == 0:
            e1, e2, e3 = P(Q.modulus()).roots(multiplicities=False)
            break
    lamb = (e3 - e1) / (e2 - e1)
    return Hp(lamb, p)


# p >= 5
def get_number_of_supersingular_curves(p):
    return round(p / 12) + {1: 0, 5: 1, 7: 1, 11: 2}[p % 12]
