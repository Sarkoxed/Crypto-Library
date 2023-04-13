from math import factorial, floor
from pprint import pprint


def drawer(l: list):
    print(sum(l[0]))
    for k in l:
        r = [str(z) for z in k]
        print("_" * 20)
        print("+".join(r))
        print()

        for z in k:
            print("* " * z)


def get_transposed(n: int):
    l = get_all_sums_naive(n, n)
    ans = []
    for _ in l:
        mm = max(len(_), _[0])
        m = ["*" * k + "_" * (mm - k) for k in _]
        if len(m) < mm:
            m += ["_" * mm] * (mm - len(m))

        flag = True
        for i in range(len(m)):
            for j in range(len(m[0])):
                if m[i][j] != m[j][i]:
                    flag = not flag
                    break
            if not flag:
                break
        if flag:
            ans.append(_)
    return ans


def get_sums_better_than_1(n):
    if n == 0:
        return []
    l = []
    for i in range(n, 1, -1):
        g = get_sums_of_odds(n - i)
        if len(g) > 0:
            for k in g:
                if 1 in k:
                    continue
                if sorted(k + [i], reverse=True) not in l:
                    l.append(sorted(k + [i], reverse=True))
        else:
            l.append([i])
    return l


def get_distinct_sums(n):
    if n == 0:
        return []
    l = []
    for i in range(n, 0, -1):
        g = get_distinct_sums(n - i)
        if len(g) > 0:
            for k in g:
                if i < k[-1]:
                    l.append(k + [i])
        else:
            l.append([i])
    return l


def get_sums_of_odds(n):
    if n == 0:
        return []
    l = []
    for i in range(n, 0, -2):
        g = get_sums_of_odds(n - i)
        if len(g) > 0:
            for k in g:
                l.append(sorted(k + [i], reverse=True))
        else:
            l.append([i])
    return l


def get_all_sums_naive(n, m):
    if n == 0:
        return []
    l = []
    for i in range(n, 0, -1):
        g = get_all_sums_naive(n - i, n)
        if len(g) > 0:
            for k in g:
                if sorted(k + [i], reverse=True) not in l:
                    l.append(sorted(k + [i], reverse=True))
        else:
            l.append([i])
    if n == m:
        k = []
        for _ in l:
            if sorted(_, reverse=True) not in k:
                k.append(sorted(_, reverse=True))
        l = k
    return l


def get_distinct_odd_num(n):
    g = get_distinct_sums(n)
    return [x for x in g if len(x) & 1]


def get_distinct_even_num(n):
    g = get_distinct_sums(n)
    return [x for x in g if not (len(x) & 1)]


def get_distinct_even_parts(n):
    g = get_distinct_sums(n)
    return [x for x in g if all(r % 2 == 0 for r in x)]


def get_distinct_odd_parts(n):
    g = get_distinct_sums(n)
    return [x for x in g if all(r % 2 == 1 for r in x)]


def get_exact_k_parts(n, k):
    l = get_all_sums_naive(n, n)
    return [x for x in l if len(x) == k]


#   checking euler theorem
# for n in range(1, 10):
#    print(len(get_distinct_odd_num(n)) - len(get_distinct_even_num(n)))

# checking for the inequality for p*(n) <= sum binomial(n - k - 1, k) for k from 0 to floor(n-1/2)
# f = []
# for i in range(2, 30):
#    print(i, end = "   ")
#    z = 0
#    for j in range(floor((i-1)/2+1)):
#        z += factorial(i - j - 1) // (factorial(j) * factorial(i - 2*j - 1))
#    p = get_sums_better_than_1(i)
#    f.append(p)
#    if(len(p) > z):
#        print(p, z)
# print("kaka")
# print(f)
# l = []
# for i in range(2, 30):
#    l.append(len(get_all_sums_naive(i)) - len(get_all_sums_naive(i-1)))
#
# for i,j in zip(f, l):
#    print(len(i), j)
# n = int(input())
# drawer(get_transposed(n))
# print("-"* 50)
# drawer(get_distinct_odd_parts(n))

# drawer(get_all_sums_naive(9, 9))

# print(len(get_all_sums_naive(9, 9)))
# print()
# drawer(get_all_sums_naive(7, 7))
# for i in range(1, 20):
#    print(len(get_transposed(i)))
for i in range(1, 20):
    print(len(get_exact_k_parts(19, i)))
