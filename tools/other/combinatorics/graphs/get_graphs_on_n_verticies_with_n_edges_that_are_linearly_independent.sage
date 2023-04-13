from itertools import combinations


def number_of_graphs(n):
    s = []
    for _ in combinations(list(range(0, n)), 2):
        x = [0] * n
        x[_[0]] = 1
        x[_[1]] = 1
        s.append(x)
    ans = 0

    for m in combinations(s, n - 1):
        v = Matrix(m).T
        if v.rank() == v.dimensions()[1]:
            ans += 1
    return ans


for i in range(1, 7):
    print(number_of_graphs(i), end=", ")
