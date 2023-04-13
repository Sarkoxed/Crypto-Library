from sage.all import *


def get_partitititit(n, k):
    if k == 0:
        return 0
    elif k == 1:
        return 1
    elif k == n:
        return 1
    else:
        return get_partitititit(n - 1, k - 1) + get_partitititit(n - 1, k) * k


def ttt(x: list):
    z = []
    n = len(x)
    #    print(x)
    for i in range(n):
        for j in range(n):
            #            print(x[i][j])
            if x[i][j] == 1:
                #    print(i, j)
                z.append((i, j))
                z.append((j, -i + n - 1))
                z.append((-i + n - 1, -j + n - 1))
                z.append((-j + n - 1, i))
    #    print(z)
    #    print(set(z))
    if len(set(z)) != n**2:
        return False
    return True


def get_ns(n):
    m = n**2 // 4
    l = binomial(n**2, m)
    ma = MatrixSpace(GF(2), nrows=n, ncols=n)
    an = []
    while len(an) != l:
        g = ma.random_element()
        n = 0
        for i in g:
            for j in i:
                if int(j) == 1:
                    n += 1
        if n == m and g not in an:
            an.append(g)

    print(an)
    an = [[list(x) for x in y] for y in an]
    an = [x for x in an if ttt(x)]
    print(an)
    return len(an)


n = int(input("n: "))
z = get_ns(n)
print(z)
print(
    get_partitititit(n**2 // 4, 4),
    get_partitititit(n**2 // 4, 1),
    get_partitititit(n**2 // 4, 3),
    get_partitititit(n**2 // 4, 2),
)
