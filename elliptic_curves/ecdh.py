from elliptic_curves import *


if __name__ == "__main__":
    p = int(input("p: "))
    a1, a2, a3, a4, a6 = [int(input(f"a{i}")) for i in [1,2,3,4,6]]
    E = EC(a1, a2, a3, a4, a6, GF(p))
    x, y = int(input("Px")), int(input("Px"))
    P = E((x, y, 1))

    na = int(input("Alice's secret key: "))
    Qa = na * P
    print(Qa)

    m1, m2 = int(input("m1 mod p: ")), int(input("m2 mod p:"))
    k = int(input("k: "))
    R = k * P
    S = k * Qa
    c1 = (S.x() * m1) % p
    c2 = (S.y() * m2) % p

    print(R, c1, c2)

    T = na * R
    m1_ = c1 * pow(T.x(), -1, p)
    m2_ = c2 * pow(T.y(), -1, p)

    print(m1_, m2_)
