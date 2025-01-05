from sage.all import PolynomialRing, GF, EllipticCurve, Zmod, randint
from polynomials_mod_prime_power import find_root
from tqdm import tqdm
import itertools

# The following three functions are probably not finding the "order" but the amount of the solutions
# It defintely does not account for solutions of the form (a : b : 0), with both a, b nonzero
# but I haven't touched (grass) elliptic curves over the rings properly yet


def brute_order_mod_prime_power(a, b, p, e):
    E = EllipticCurve(Zmod(p**e), [a, b])
    order = 1
    # for g in tqdm(range(p**e)):
    for g in range(p**e):
        tmp = (g**3 + a * g + b) % p**e
        y_vals = find_root((-tmp, 0, 1), p, e)
        order += len(y_vals)
    return order


def bruuute_order_mod_prime_power(a, b, p, e):
    order = 1
    for x in tqdm(range(p**e)):
        for y in range(p**e):
            tmpr = (x**3 + a * x + b) % p**e
            tmpl = pow(y, 2, p**e)
            order += tmpr == tmpl
    return order


# Multivariate Hensel's lemma: (3 * x0**2 + a) * t2 - 2 * y0 * t1 = ((y0**2 - (x0**3 + a * x0 + b)) / p) (mod p)
def find_order_mod_prime_2(a, b, p, e=2):
    e = EllipticCurve(GF(p), [a, b])
    initial_order = e.order()

    P = PolynomialRing(GF(p), "x")
    x = P.gens()[0]

    # keep track of used special values
    new_order = 1
    used_vals = 1

    y0_encountered = []
    # handle (3 * x0**2 + a) = 0 case
    s1 = 3 * x**2 + a
    for x0, _ in s1.roots():
        print("I was here")
        tmp = x0**3 + a * x0 + b
        if not tmp.is_square():
            continue

        used_vals += 1
        y0 = tmp.sqrt()
        if y0 == 0:
            print("and here")
            y0_encountered.append(x0)
            rhs = ((int(y0) ** 2 - (int(x0) ** 3 + int(a) * int(x0) + int(b))) // p) % p
            if rhs == 0:
                # we have 0 * t2 - 0 * t1 = 0 (mod p) => p^2 solutions
                new_order += p**2
            else:
                # 0 * t2 - 0 * t1 = smth (mod p) => 0 solutions
                continue
        print("Here too")
        # 0 * t2 - 2 * y0 * t1 = smth -> p solutions
        # 0 * t2 + 2 * y0 * t1 = smth -> p solutions
        used_vals += 1
        new_order += 2 * p

    # handle y0 = 0 case
    s1 = x**3 + a * x + b
    for x0, _ in s1.roots():
        print("I was here too")
        if x0 in y0_encountered:
            continue

        # 0 * t2 - 0 * t1 = 0/smth can't be here, since we've handled it earlier
        # hence it's only (3 * x0^2 + a) * t2 - 0 * t1 = smth -> p solutions
        used_vals += 1
        new_order += p

    # for every other case we have
    # (3 * x0^2 + a) * t2 - 2 * y0 * t1 = smth, where none of the coefficients is not 0 mod p => p solutions
    new_order += (initial_order - used_vals) * p
    return new_order


def lift_point_to_p_2(x, y, a, b, p):
    G = GF(p)
    tmp1 = G(3 * x**2 + a)
    tmp2 = G(2 * y)
    rhs = G((int(y) ** 2 - (int(x) ** 3 + int(a) * int(x) + b)) // p)

    lifts = []
    if tmp1 == 0:
        if tmp2 == 0:
            if rhs == 0:
                return [
                    (x + t1 * p, y + t2 * p)
                    for t1, t2 in itertools.product(range(p), repeat=2)
                ]
            return []

        t = int(rhs * pow(-tmp2, -1))
        return [(x + t1 * p, y + t * p) for t1 in range(p)]

    if tmp2 == 0:
        t = int(rhs * pow(tmp1, -1))
        return [(x + t * p, y + t1 * p) for t1 in range(p)]

    tmp2 = tmp2 * pow(tmp1, -1)
    rhs = rhs * pow(tmp1, -1)

    return [(x + int(t1 * tmp2 + rhs) * p, y + t1 * p) for t1 in range(p)]


def test_all_the_solutions():
    for a, b in tqdm(list(itertools.product(range(p), repeat=2))):
        if (4 * a**3 + 27 * b**2) % p == 0:
            continue
        r1 = brute_order_mod_prime_power(a, b, p, 2)
        # r2 = (bruuute_order_mod_prime_power(a, b, p, 2))
        r3 = find_order_mod_prime_2(a, b, p, 2)

        # if len(set([r1, r2, r3])) != 1:
        if len(set([r1, r3])) != 1:
            print(p, a, b)
            break


def test_lifting():
    E = EllipticCurve(GF(p), [a, b])
    e = E.random_point()

    print(find_order_mod_prime_2(a, b, p))

    x, y = int(e[0]), int(e[1])
    new_points = lift_point_to_p_2(x, y, a, b, p)

    E1 = EllipticCurve(Zmod(p**2), [a, b])
    for point in new_points:
        print(E1(point))


mod = 101**2
p = 101
a = -1
b = 18
