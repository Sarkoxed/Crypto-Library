# 1 1 2 2 3 3 4 4 5 5 6 6 ... n n 
# ro(1, 1) in perm is 1
# ro(2, 2) is 2
# ...

# ex0: 3 1 2 1 3 2      and it's reverse
# ex1: 4 1 3 1 2 4 3 2  and it's reverse

# n = 0 or n = 3 mod 4
# sum(first index of i in perm, for i in [1..n]) = n * (3 * n - 5) / 4
# on the other hand it's a Partition of n * (3 * n - 5) / 4 into n distinct numbers, that are bounded by 2n - 3, and 0, 1 are present
# but since 0 is not included in Partitions we can add 1 to each index to make it a proper partition of
# n * (3 * n - 5) / 4 + n into n distinct bounded elements

# ah, yes apparently it's called A Langord pairing

from sage.all import Partitions
from itertools import permutations

# dumb method

def is_good(p, i):
    c = p.index(i)
    c1 = p.index(i, c + 1)
    return c1 - c == i + 1

def find(n, all=False):
    init = list(range(1, n + 1)) * 2
    res = set()
    for p in permutations(init):
        if all(is_good(p, i) for i in range(1, n+1)):
            res.append(p)
            if not all:
                print(p)
                return
            else:
                res.add(p)
    return set(res)

# quiet more advanced
def get_partitions(n):
    tmp = n * (3 * n - 5)
    assert tmp % 4 in [0, 3]
    tmp //= 4
    for p in Partitions(tmp + n):
        if len(p) != n:
            continue
        if len(set(p)) != n:
            continue
        if 1 not in p:
            continue
        if 2 not in p:
            continue
        if 2 * n in p:
            continue
        if 2 * n - 1 in p:
            continue
        print(p)

print(get_partitions(7))
