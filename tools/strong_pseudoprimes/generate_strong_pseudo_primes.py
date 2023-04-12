# https://core.ac.uk/download/pdf/81930829.pdf

from sage.all import (
    prime_range,
    legendre_symbol,
    crt,
    lcm,
    is_prime,
    next_prime,
    random_prime,
    product,
    var,
    PolynomialRing,
    GF,
    factor,
    lift,
)

from copy import copy, deepcopy
from random import choice

basis78 = list(prime_range(10000))


def miller_rabin(n, b):
    """
    Miller Rabin test testing over all
    prime basis < b
    """
    basis = [x for x in basis78 if x <= b]
    if n == 2 or n == 3:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for b in basis:
        x = pow(b, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def get_sets_a_ki(k, Sa, A):
    return [
        set([(pow(k, -1, 4 * a) * (x + k - 1)) % (4 * a) for x in Sa[a]]) for a in A
    ]


def getSa(A, Bound=2**20):
    return {
        a: set(
            [p % (4 * a) for p in prime_range(3, Bound) if legendre_symbol(a, p) == -1]
        )
        for a in A
    }


def get_ks(m, A, Sa, H, scale):
    while True:
        H1 = deepcopy(H)
        ks = [random_prime(lbound=max(A) + 1, n=max(A) * scale) for _ in range(m - 1)]
        if len(set(ks)) != m - 1:
            continue

        for k in ks:
            Hi = get_sets_a_ki(k, Sa, A)
            for i, sk in enumerate(Hi):
                tmp = H1[i].intersection(sk)
                if len(tmp) == 0:
                    break
                H1[i] = tmp
            else:
                continue
            break  # exit if the loop was broken
        else:
            r1, r2 = 0, 0
            for u in H1:
                # checks that there's a valid number of choices to build
                # a "prime" using crt
                tmp = [x % 4 for x in u]
                r1 += 1 in tmp
                r2 += 3 in tmp

            if r1 != len(A) and r2 != len(A):
                continue

            if ki_cond([1] + ks, m) is not None:
                # checks that there're roots of f_i(x) mod k_i
                break

    return ks, [list(h) for h in H1]


def get_unions(ks, Sa, A, H1):
    for k in ks:
        Hi = get_sets_a_ki(k, Sa, A)
        for i, sk in enumerate(Hi):
            tmp = H1[i].intersection(sk)
            if len(tmp) == 0:
                break
            H1[i] = tmp
        else:
            continue
        break
    return H1


def req_sols(unions, state, A, k=1000):
    if len(state) == len(A):
        try:
            p1 = crt(state, A)
            return [(p1, tuple(state))]
        except ValueError:
            return None

    res = []
    for s in unions[0]:
        if len(state) > 1 and s % 4 != state[-1] % 4:
            continue
        p = req_sols(unions[1:], state + [s], A)
        if p is not None:
            res += p

            if len(res) >= k:  # stop after some number of valid solutions
                break
    return res


def ki_cond(ks, m):
    if m == 3:
        return [pow(-ks[2], -1, ks[1]), pow(-ks[1], -1, ks[2])]  # f_i(x) always have root mod ki since it's linear

    conds = []
    x = var("x")
    for i in range(1, m):
        kmod = ks[i]

        P = PolynomialRing(GF(kmod), x)
        poly = product(P(ks[j] * (x - 1) + 1) for j in range(m) if j != i)
        poly -= 1
        poly //= P(x-1)

        roots = poly.roots()
        if len(roots) == 0:
            return None
        print(roots)
        conds.append(choice(roots)[0]) # TODO I do not want to handle this NOW
    return [lift(c) for c in conds]


def generate(
    A, z_s, ks, num_pspr=10, step=1, step_Bound=2**20, miller_rabin_Bound=64
):
    pspr = []
    extra_ki_condition = ki_cond(ks, len(ks))
    mod = lcm([4 * a for a in A])

    for z in z_s:
        p1, chosen = z
        
        print(z)
        print(extra_ki_condition)
        print(mod)
        
        p1 = crt([p1] + extra_ki_condition, [mod] + ks[1:])  # 3d case
        mod1 = lcm([mod] + ks[1:])
        counter = 0

        flag_multiplier_bound = False

        while True:
            flag_not_all_primes = False

            ps = []
            for k in ks:  # first is just p1
                pi = k * (p1 - 1) + 1
                if not miller_rabin(pi, miller_rabin_Bound): # TODO maybe use is_prime?
                    p1 += step * mod1
                    counter += 1
                    if counter > step_Bound:
                        flag_multiplier_bound = True
                        break
                    flag_not_all_primes = True
                    break
                ps.append(pi)

            if flag_multiplier_bound:
                break

            if not flag_not_all_primes:  # all primes found
                break

        if flag_multiplier_bound:  # go to next choice of z_a's
            continue

        if miller_rabin(product(ps), len(A)):
            pspr.append(ps)
            if len(pspr) == num_pspr:
                return pspr
        else:
            print("OBOSRALSYA")
    return pspr


def generate_strong_pseudo_primes(
    base_n,
    num_pf,
    scale=5,
    req_stop=50,
    num_primes=20,
    step=1,
    step_Bound=2**20,
    m_r_Bound=64,
):
    A = list(prime_range(base_n)) # may be changed to arbitrary bases
    Sa = getSa(A)
    k1 = 1
    print("preps done")

    H1 = get_sets_a_ki(k1, Sa, A)
    ks, Unions = get_ks(num_pf, A, Sa, copy(H1), scale)
    ks = [k1] + ks

    print("ks: ", ks)
    print("Unions done")

    z_s = req_sols(Unions, [], [4 * a for a in A], req_stop)
    # works most of the time/except for hard paths

    print(len(z_s), " z's found")

    strong_primes = generate(A, z_s, ks, num_primes, step, step_Bound, m_r_Bound)
    primes = [product(x) for x in strong_primes]

    return ks, primes, strong_primes


if __name__ == "__main__":
    n = 30
    m = 5
    k, pr, facs = generate_strong_pseudo_primes(n, m, 30, step=1)
    print(pr)
