from copy import copy


def get_triangles(l):
    if len(l) == 0:
        return []
    z = get_triangles(l[1:])
    ans = []
    for i in range(pow(2, len(l) - 1)):
        r = bin(i)[2:].zfill(len(l))
        r = [int(x) for x in r]
        if r.count(1) <= l[0]:
            # print(i, r)
            if len(r) == 1:
                ans.append([r])
                # print(ans, "null")
            else:
                for j in z:
                    ans.append([r] + j)
    return ans


def get_graphs_naive(deg):
    triangles = get_triangles(deg)
    for i in range(len(triangles)):
        for j in range(len(triangles[0])):
            f = triangles[i][j]
            triangles[i][j] = [0] * (len(triangles[0]) - len(f)) + f
    for i in range(len(triangles)):
        for j in range(len(triangles[0])):
            for k in range(j + 1, len(triangles[0][0])):
                if triangles[i][j][k]:
                    triangles[i][k][j] = 1
    ans = []
    for j in triangles:
        v = [sum(j[i]) for i in range(len(j))]
        if v == deg:
            ans.append(tuple(j))
    return ans


def get_graph(deg: list):
    # print(deg, "beg")
    if all(i == 0 for i in deg):
        return 1, []
    z = [(i, j) for i, j in enumerate(deg) if j != 0]
    if any(x[1] >= len(z) for x in z):
        return 0, []
    for i in z[1:]:
        deg1 = [y - 1 if x in (z[0][0], i[0]) else y for x, y in enumerate(deg)]
        # print(deg1, "first skip")
        rez, l1 = get_graph(deg1)
        if rez:
            # print(l1)
            if (z[0][0], i[0]) not in l1:
                l1.append((z[0][0], i[0]))
                break

    return rez, l1


from time import time

x = time()
print(get_graph([3] * 11))
x = time() - x
print(x)
