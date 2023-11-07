#! sage
# also it better works in sage
# own observations:

# len   prec    t          d
# 1     4+-1    10         4+-2
# 2     6+-2    10^(1+-2)  6+-2
# 3     8+-2    10^(1+-2)  8+-2
# 4     10+-2   10^(1+-2)  10+-2
# 5     12+-2   10^(2+-1)  12+-2
# 6     15+-2   10^(3+-1)  15+-2
# 7     17+-2   10^(4+-1)  17+-2
# 8     19+-2   10^(5+-1)  19+-2
# 9     20+-2   10^(5+-1)  20+-2

# 500   1000+-4 10^(333+-4) 1000+-4

# d ~ O(2 * len)
# a ~ O(2 * len / 3) (?)
# prec ~ O(len * 2)
#
# however if precision is sufficiently large than t --> 1
# get_least_power(randint(10**99, 10**100-1), 1000) - (0, 1995)


def get_appr(lens_bound):
    di = dict()
    for j in range(2, lens_bound):
        for k in range(10):
            i = randint(10 ** (j - 1), 10**j - 1)
            di[i] = []
            for d in range(1, 2 * len(str(i)) + 10):
                z = get_least_power(i, d)
                if z is not None:
                    print(i)
                    di[i].append((len(str(i)), d, z[0], z[1]))
                    break
    return di


def get_least_power(n, d):
    alpha = floor((pow(n, 1 / 3) - floor(pow(n, 1 / 3))) * 10**d) / 10**d
    for di in range(len(str(n)) // 4, len(str(n)) + 10):
        for r in range(d1 - 5, d1 + 5):
            m = Matrix(
                [
                    [10**di, 0, 0, 0, floor(10**r * alpha)],
                    [0, 1, 0, 0, floor(10**r * alpha**2)],
                    [0, 0, 1, 0, floor(10**r * alpha)],
                    [0, 0, 0, 1, 10**r],
                ]
            )

            v = m.LLL()[0]

            if abs(v[0]) != 10**di:
                continue

            sign = v[0] / 10**di
            A, B, C = v[1] * sign, v[2] * sign, v[3] * sign

            b = A // 3

            if 3 * b**2 != B:
                continue

            if b**3 - C != n:
                continue

            return (d, r)


# this works in critical point when precision is low
def get_number(a, prec, lenb):
    a = a / 10**prec

    for t in range(prec // 3 - 10, lenb):
        for d in range(2 * lenb - 10, 2 * lenb + 10):
            m = identity_matrix(4)
            m[0, 0] = 10**t

            m = m.T.insert_row(
                4, vector([floor(10**d * a ** (3 - i)) for i in range(4)])
            ).T

            v = m.LLL()[0]
            if not abs(v[0]) % 10**t == 0 or v[0] == 0:
                continue

            sign = v[0] // 10**t

            A = v[1] * sign
            B = v[2] * sign
            C = v[3] * sign

            b = A // 3

            if not 3 * b**2 == B:
                continue

            K = b**3 - C
            return K


if __name__ == "__main__":
    a, d, b = (
        int(input("alpha: ")),
        int(input("prec: ")),
        int(input("appr len of primary integer in decimal: ")),
    )
    print(get_number(a, d, b))
