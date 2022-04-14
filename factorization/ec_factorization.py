from sage.all import *
import re

def ec_factor(n: int):
    while True:
        A = randint(1, n)
        a, b = randint(1, n), randint(1, n)
        B = int((b**2 - a**3 - A*a) % n)
        while not ((4*A**3 + 27*B**2) % n):
            a, b = randint(1, n), randint(1, n)
            B = int((b**2 - a**3 - A*a) % n)

        E = EllipticCurve(IntegerModRing(n), [A, B])
        P = E((a, b))
        Q = P
        for i in range(2, ceil(sqrt(n))):
            try:
                Q1 = i * P
                P = Q1
            except Exception as e:
                x = int(re.search(r"[0-9]+", str(e)).group(0))
                d = gcd(x, n)
                if(d == 1 or d == n):
                    break
                else:
                    return d
            Q = Q1


if __name__ == "__main__":
    for i in [589, 26167, 1386493, 28102844557]:
        k = ec_factor(i)
        print(i, k, i//k, k * (i//k))

