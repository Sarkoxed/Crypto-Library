from sage.all import (
    GF,
    PolynomialRing,
    ceil,
    divisors,
    factor,
    floor,
    lcm,
    gcd,
    log,
    product,
    var,
    euler_phi,
)
from time import time


def get_ring_order_dumb(Q):  # based
    a = 0
    for e in Q:
        a += e.is_unit()
    return a


def get_ring_orders_dumb(Q, order):  # based
    orders = set()
    for e in Q:
        if e.is_unit():
            ei = e
            for j in range(1, order + 1):
                if ei == 1:
                    orders.add(j)
                    break
                ei *= e
    return orders


def get_ring_order(Q): # |F[x] / (f1^e1 * f2^e2 ... * fk^ek)| = \prod p^(deg(fi)*(ei - 1)) * (p^deg(fi) - 1)
    facs = list(factor(Q.modulus()))
    p = Q.base_ring().characteristic()

    ords = []
    for f, power in facs:
        d = f.degree()
        ords.append(pow(p, d * (power - 1)) * (pow(p, d) - 1))
    return product(ords)


def get_ring_orders(Q): # Orders in subring F[x] / (fi^ei) are the divisors of p^r * (p^n - 1) 
                        # where r is the smallest number such that p^r <= ei < p^(r + 1)
                        # https://math.stackexchange.com/questions/4666368/orders-of-all-the-elements-in-polynomial-quotient-ring/4666790#4666790
                        # so all the orders are the divisors of LCM(p^ni - 1, p^max(ri)), note ri != ni * (ei - 1) all the time
    facs = list(factor(Q.modulus()))
    p = Q.base_ring().characteristic()
    ns, es = [f.degree() for f, _ in facs], [e for _, e in facs]

    rs = []
    for e in es:
        r = floor(log(e) / log(p))
        if pow(p, r) < e:
            rs.append(r + 1)
        else:
            rs.append(r)
    R = max(rs)
    return divisors(lcm([pow(p, n) - 1 for n in ns] + [pow(p, R)]))


def get_ring_orders2(Q): # Second method using the exact subring order
    facs = list(factor(Q.modulus()))
    p = Q.base_ring().characteristic()
    ns, es = [f.degree() for f, _ in facs], [e for _, e in facs]

    ords = [get_subring_orders(p, n, e) for n, e in zip(ns, es)]
    return divisors(lcm(ords))


def get_subring_orders(p, n, e): # https://math.stackexchange.com/questions/4666368/orders-of-all-the-elements-in-polynomial-quotient-ring/4666790#4666790
    xs = [p**n - 1]
    i = 0
    while e > pow(p, i):
        s = n * (
            ceil(e / pow(p, i))
            - 2 * ceil(e / pow(p, (i + 1)))
            + ceil(e / pow(p, (i + 2)))
        ) # degree of the inner product of (Z_p^i)^s
        i += 1
        if s != 0:
            xs.append(pow(p, i))
    return lcm(xs)


def get_ring_decomposition(
    Q,
):  # returns an array corresponding to F[x]/f(x) = F_i[x] / f_i(x)^e_i
    # F_i[x] / f_i(x)^e_i = Z_{p^n_i - 1} * Z_p ^ s_1 * Z_p2 ^ s_2 * ...
    facs = list(factor(Q.modulus()))
    p = Q.base_ring().characteristic()
    ns, es = [f.degree() for f, _ in facs], [e for _, e in facs]

    res = []
    m = len(facs)

    for i in range(m):
        n = ns[i]
        e = es[i]
        tmp = [facs[i][0], n, e]

        orders = [p**n - 1]

        i = 0
        powers = [1]
        while e > pow(p, i):
            s = n * (
                ceil(e / pow(p, i))
                - 2 * ceil(e / pow(p, (i + 1)))
                + ceil(e / pow(p, (i + 2)))
            )

            if s != 0:
                powers.append(s)
                orders.append(pow(p, i + 1))
            i += 1

        tmp.append(orders)
        tmp.append(powers)
        res.append(tmp)

    return res


def get_ring_structure_dumb(Q):
    res = get_ring_decomposition(Q)

    min_order = lcm(res[0][3])
    for i in range(1, len(res)):
        min_order = lcm(res[i][3] + [min_order])

    possible_orders = divisors(min_order)

    els = {x: 0 for x in possible_orders}
    for q in Q:
        if q.is_unit():
            for order in possible_orders:
                if pow(q, order) == 1:
                    els[order] += 1
                    break

    assert sum(els.values()) == get_ring_order(Q)
    return els

def req_numbers(orders, K): # find all the elements s.t. lcm(a1, a2, ..., an) == K and ai | orders[i]
    pass

def number_of_els(free_args, zpows, k):
    pos_orders = [gcd(x, k) for x in free_args if gcd(x, k) == 1]

    pos_zpows = dict()
    for p in zpows:
        t = gcd(p, k)
        pos_zpows[t][1] += zpows[p]  # number of elements in vector of elements with order p^k

    mp = max(pos_zpows.keys())
    if 1 not in pos_zpows:
        np = req_p(pos_zpows, mp)

    nf = req_numbers(pos_orders, k // mp)
    return nf * np


def get_ring_structure(
    Q,
):  # returns the number of elements corresponding to the particular order
    res = get_ring_decomposition(Q)

    min_order = lcm(res[0][3])
    for i in range(1, len(res)):
        min_order = lcm(res[i][3] + [min_order])

    possible_orders = divisors(min_order)
    p = Q.base_ring().characteristic()

    free_args = []  # all the Z_{p^n - 1}
    zpows = dict()  # all the Z_p^k ^ r
    for ki in res:
        free_args.append(ki[3][0])
        for t in range(1, len(ki[3])):
            _ = zpows.setdefault(
                ki[3][t],
            )
            zpows[ki[3][t]] += ki[4][t]

    els = {x: 0 for x in possible_orders}
    for k in possible_orders:
        els[k] = number_of_els(free_args, zpows, k)

    return els


if __name__ == "__main__":
    x = var("x")
    P = PolynomialRing(GF(3), x)
    f = P.random_element(degree=9)
    print(factor(f))
    Q = P.quo(f)

    start = time()
    o = get_ring_order_dumb(Q)
    print(o)
    if o < 10000:
        ords = sorted(list(get_ring_orders_dumb(Q, o)))
        print(ords)
        print(time() - start)
        print()

        start = time()
        o = get_ring_order(Q)
        ords = get_ring_orders(Q)
        print(o)
        print(sorted(list(ords)))
        print(time() - start)
        print()

        start = time()
        print(get_ring_orders_aboba(Q))
        print(time() - start)
