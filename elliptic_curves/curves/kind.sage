from time import sleep

from factordb import FactorDB


def get_ec_type(a, b, p, e = 1):
    G = GF(p)
    if G(4 * a**3 + 27 * b**2) == G(0):
        x = var("x")
        P = PolynomialRing(G, x)
        f = P(x**3 + a * x + b)
        r = f.roots()
        if len(r) == 1:
            return f"Singular EC homomorphic to y^2 = x^3. Root: {r[0][0]}"
        x = r[1][0]
        if pow(x, (p - 1) // 2, p) == 1:
            return f"Singular EC homomorphic to y^2 = x^2 * (x + a) over GF(p). a: {r[1][0]}"
        return (
            f"Singular EC homomorphic to y^2 = x^2 * (x + a) over GF(p^2). a: {r[1][0]}"
        )

    e = EllipticCurve(GF(p), [a, b])
    q = e.order()

    if is_prime(q):
        if q == p:
            return "Anomalous EC"
        return "EC of prime order"

    fac = FactorDB(int(q))
    fac.connect()
    print("sleeping for a moment...")
    sleep(10)
    fac = FactorDB(int(q))
    facs = fac.factor_list()

    newfacs = []
    for i in facs:
        while True:
            alarm(30)
            try:
                print("factoring..")
                c = factor(i)
                newfacs += [x[0] for t in range(x[1]) for x in c]
            except KeyboardInterrupt as KI:
                print("timed out!")
                newfacs.append(i)
            alarm(0)
    return "EC of the order {q} which factors to {newfacs}"


if __name__ == "__main__":
    p = int(input("p: "))
    a = int(input("a: "))
    b = int(input("b: "))
    print(get_ec_type(a, b, p))
