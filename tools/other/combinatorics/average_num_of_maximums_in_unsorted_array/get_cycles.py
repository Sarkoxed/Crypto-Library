from sage.all import factorial
from gmpy2 import mpq


def req(n, k):
    if k == 0:
        if n == 0:
            return 1
        return 0
    elif k == 1:
        return factorial(n - 1)
    elif k == n:
        return 1
    elif k > n:
        return 0
    return req(n - 1, k - 1) + (n - 1) * req(n - 1, k)


# it returns the amount of maps only containing cycles of the lengths in degs. For example: 4, [2, 1]  will return the amount of permutations of 4 elements with cycles of length 1 and 2 only
# have to be improved for the case cur == len(degs) -1
def cycle_structure(n: int, degs: list[int], cur_sum: int = 0, cur: int = 0) -> mpq:
    if cur == 0:
        cur_sum = n

    if cur == len(degs) - 1:
        return 1

    res = mpq(0)
    for kn in range(cur_sum // degs[cur] + 1):
        if cur == len(degs) - 2:
            res += mpq(
                1, degs[cur] ** kn * factorial(kn) * factorial(cur_sum - degs[cur] * kn)
            )
        else:
            res += mpq(1, degs[cur] ** kn * factorial(kn))

        res *= cycle_structure(n, degs, cur_sum - degs[cur] * kn, cur + 1)

    if cur == 0:
        return res * factorial(n)
    return res

if __name__ == "__main__":
    # print(req(int(input("n ")), int(input("k "))))
    # for i in range(5):
    #    print(f"[{4}, {i}] = {req(4, i)}")
    
    print(cycle_structure(4, [4]))
