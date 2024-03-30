# Fast Collision Attack on MD5.pdf

from math import log2


def int_to_bin(X, n):
    return [int(xi) for xi in bin(X)[2:].zfill(n)]


def bin_to_int(X):
    return sum(xi * 2**i for i, xi in enumerate(X[::-1]))


def delta_xor(X, X_prime):
    return [x ^ y for x, y in zip(X, X_prime)]


def delta_int_mod(X, X_prime):
    n = len(X)
    x = bin_to_int(X)
    x_p = bin_to_int(X_prime)
    delta = (x - x_p) % 2**n
    return int_to_bin(delta, n)


def delta_sub(X, X_prime):
    return [x - y for x, y in zip(X, X_prime)]


def weight(dX):
    return len(dX) - dX.count(0)


def deltas(dX):
    return [2**i for i in range(len(dX)) if dX[::-1][i]]


# number of signed differences for delta_i = 2**k
# e.g for dX = 1000001, delta_1 = 1, delta_2 = 2**6, for delta_1 there're exactly 6 of them:
# 1000001
# 100001-1
# 10001-1-1
# 1001-1-1-1
# 101-1-1-1-1
# 11-1-1-1-1-1
# same goes to the highest but with 2**n
def nus(dX):
    n = len(dX)
    nus = []
    delt = deltas(dX)
    w = weight(dX)
    for i in range(len(delt)):
        if i == w - 1:
            nus.append(n - int(log2(delt[i])))
        else:
            nus.append(int(log2(delt[i + 1] // delt[i])))
    return nus


def sub_to_xor(dX):
    return [abs(x) for x in dX]


def sub_to_int_mod(dX):
    n = len(dX)
    delta = bin_to_int(dX) % 2**n
    return int_to_bin(delta, n)


# not exactly bijective cause +- 2**(n - 1) = 2**(n - 1) \pmod{2**n}
def xor_int_mod_to_sub(dX_xor, dX_mod):
    n = len(dX_xor)
    dX = [0 for _ in range(n)]

    t = bin_to_int(dX_mod)
    flag = True

    for i in range(n):
        if dX_xor[i] == 0:
            continue

        if i == 0:  # highest bit always 1
            dX[i] = 1
            t -= 2 ** (n - 1)
            flag = False
            continue

        cur_pow = 2 ** (n - i - 1)

        if flag:  # first nonzero bit check for overflow
            flag = False
            if t - cur_pow > cur_pow:
                t -= 2**n
            # print(t, flag)

        if -cur_pow < (t - cur_pow) < cur_pow:
            dX[i] = 1
            t -= cur_pow
        else:
            dX[i] = -1
            t += cur_pow

        assert -cur_pow < t < cur_pow

    assert bin_to_int(dX) % 2**n == bin_to_int(dX_mod)

    if dX_xor[0] == 1:  # +- 2**(n-1) doesn't change the sum
        dX1 = dX.copy()
        dX1[0] = -1
        assert bin_to_int(dX1) % 2**n == bin_to_int(dX_mod)
        return dX, dX1

    return (dX,)
