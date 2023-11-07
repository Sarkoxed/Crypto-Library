from sage.all import *

# my ovn observation is that:
# 
# the number t(which is 0,0 in matrix is 10**(O(len(str(K))/2))
# d = O(len(str(K)))

def get_least_power(n1, d1):
    n = floor((pow(n1, 1 / 2) - floor(pow(n1, 1 / 2))) * 10**d) / 10**d1
    for d in range(1, len(str(n)) + 10):
        for r in range(1, d1 + 10):
            m = Matrix(
                [
                    [1, 0, 0, floor(10**r * n**2)],
                    [0, 1, 0, floor(10 * n)],
                    [0, 0, 1, 10**r],
                ]
            )
            v = m.LLL()[0]
            if abs(v[0]) != 10**d:
                continue
            sign = v[0] / 10**d
            A, B, C = v[1] * sign, v[2] * sign, v[3] * s

            b = A // 3
            if 3 * b**2 != B:
                continue
            if b**3 - C != n1:
                continue
            return (d, r)


def get_number(a, B):
    m = identity_matrix(3)
    m[0, 0] = 10 ** (B // 2)

    m = m.T.insert_row(
        3, vector([floor(10 ** (B + 2) * a ** (2 - i)) for i in range(3)])
    ).T

    print(m)
    print()
    print(m.LLL())
    v = m.LLL()[0]
    assert abs(v[0]) % 10 ** (B // 2) == 0
    sign = v[0] // 10 ** (B // 2)
    A = v[1] * sign
    B = v[2] * sign
    b = A // 2
    K = b**2 - B
    return K


if __name__ == "__main__":
    a, b = float(input("alpha: ")), int(
        input("appr len of primary integer in decimal: ")
    )
    print(get_number(a, b))
