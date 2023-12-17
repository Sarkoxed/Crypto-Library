from sage.all import EllipticCurve, GF, random_prime, randint, ceil, factor, lcm, sqrt
from Crypto.Util.number import getPrime

# This works only for E(F_p), however you can find the order of E(F_p^n) later, 
# using requrcive relation


def get_nullifier(P):
    p = P.base_ring().order()

    m = p.nth_root(4, truncate_mode=True)[0] + 1

    ps = dict()
    start = P * 0
    for j in range(m + 1):
        if start[0] in ps:
            for x in ps[start[0]]:
                if x * P == start:
                    return j - x

        r = ps.setdefault(start[0], [])
        r.append(j)
        ps[start[0]] = r

        start += P


    Q = (p + 1) * P
    step = 2 * m * P
    start = Q - m * step
    M1, M2 = None, None
    
    for k in range(-m, m + 1):
        if start[0] in ps:
            for x in ps[start[0]]:
                tmp = x * P
                if tmp == start:
                    M = p + 1 + 2 * m * k - x
                    return M
                elif -tmp == start:
                    M = p + 1 + 2 * m * k + x
                    return M
        start += step
        
    raise ValueError("Not enough values in the list, try larger m")

def get_point_order(P):
    M = get_nullifier(P)

    for p, e in factor(M):
        while e:
            m1 = M // p
            if m1 * P != 0:
                break
            M = m1
            e -= 1
    return M

def get_curve_order(E, k=10):
    p = E.base_ring().order()
    if p <= 229:
        return "Do it by hand, please"

    if p in [3, 4, 5, 7, 9, 11, 13, 17, 19, 23, 25, 27, 29, 31, 37, 43, 61, 73, 181, 331, 547]:
        return "Do it by hand, please"

    E1 = E.quadratic_twist()

    s1 = lcm(get_point_order(E.random_element()) for _ in range(k))
    s1_factors = []
    k = 1

    while k * s1 < p + 1 + 2 * sqrt(p):
        tmp = k * s1
        if tmp >= p + 1 - 2 * sqrt(p):
            s1_factors.append(k * s1)
        k += 1

    if len(s1_factors) == 1:
        return s1_factors[0]


    s2 = lcm(get_point_order(E1.random_element()) for _ in range(k))
    s2_factors = []
    k = 1

    while k * s1 < p + 1 + 2 * sqrt(p):
        tmp = k * s1
        if tmp >= p + 1 - 2 * sqrt(p):
            s2_factors.append(k * s1)
        k += 1

    if len(s2_factors) == 1:
        N = s2_factors[0]
        a = p + 1 - N
        return p + 1 + a

    return s1_factors, s2_factors

p = getPrime(60)
g = GF(p)
a, b = g.random_element(), g.random_element()
e = EllipticCurve(g, [a, b])

print(get_curve_order(e))
print(e.order())
