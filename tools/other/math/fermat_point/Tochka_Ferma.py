from sympy import *


def tochka_Ferma(a, b, c):
    if type(a) == float:
        if (a + b < c) or (a + c < b) or (b + c < a):
            return "poshel naxyi"
        cosa = (S(c) ** 2 - S(a) ** 2 - S(b) ** 2) / (2 * S(a) * S(b))
        sina = sqrt(1 - cos**2)
        x, y, z = S(a), S(c), S(b)
        c = [S(c) * cosa, S(c) * sina]
        a = [S(0), S(0)]
        b = [S(0), S(a)]

    else:
        a = [S(a[0]), S(a[1])]
        b = [S(b[0]), S(b[1])]
        c = [S(c[0]), S(c[1])]
        print(a, b, c)
        print(a, b, c)  #################

        if a[1] > b[1]:
            b, a = a, b
        if a[1] > c[1]:
            c, a = a, c

        print(a, b, c)  ##########################################

        p1 = a[0]
        p2 = a[1]

        b = [b[0] - a[0], b[1] - a[1]]
        c = [c[0] - a[0], c[1] - a[1]]
        a = [S(0), S(0)]

        print(a, b, c)  ##########################################

        if b[0] < c[0]:
            b, c = c, b

        print(a, b, c)  ##########################################

        if b[0] == a[0]:
            phi = -S(pi)
        else:
            phi = atan(b[1] / b[0])

        print(phi)  ##########################################

        b = [b[0] * cos(phi) - b[1] * sin(phi), b[0] * sin(phi) + b[1] * cos(phi)]
        c = [c[0] * cos(phi) - c[1] * sin(phi), c[0] * sin(phi) + c[1] * cos(phi)]

        print(a, b, c)  ##########################################

        x = b[0]
        y = sqrt((a[0] - c[0]) ** 2 + (a[1] - c[1]) ** 2)
        z = sqrt((c[0] - b[0]) ** 2 + (c[1] - b[1]) ** 2)
        if (x + y < z) or (x + z < y) or (z + y < x):
            print("kusok govna")

        print(x, y, z)  ##########################################

        M = [x / 2, -1 * x * sqrt(S(3)) / 2]
        N = [
            (c[0] - x) * cos(-S(pi) / 3) - c[1] * sin(-S(pi) / 3) + x,
            (c[0] - x) * sin(-S(pi) / 3) + c[1] * cos(-S(pi) / 3),
        ]

        print(M, N)  ##########################################

        if M[0] != c[0]:
            x1 = (-c[1] + c[0] * (M[1] - c[1]) / (M[0] - c[0])) / (
                (M[1] - c[1]) / (M[0] - c[0]) - N[1] / N[0]
            )
            y1 = N[1] * x1 / N[0]
        elif M[0] == c[0]:
            x1 = c[0]
            y1 = N[1] / N[0] * c[0]

        print(x1, y1)  ##########################################

        print(
            (
                x1 * cos(-1 * phi) - y1 * sin(-1 * phi) + p1,
                x1 * sin(-1 * phi) + y1 * cos(-1 * phi) + p2,
            )
        )
        return (
            x1 * cos(-1 * phi) - y1 * sin(-1 * phi) + p1,
            x1 * sin(-1 * phi) + y1 * cos(-1 * phi) + p2,
        )


if __name__ == "__main__":
    a = float(input())
    b = float(input())
    c = float(input())
    a = [2, 1]
    b = [4, 2 * sqrt(S(3)) + 1]
    c = [6, 1]
    print(tochka_Ferma(a, b, c))
