from sage.all import binomial, factorial


def req(n: int, k: int):
    if k > n:
        return 0
    elif k == n:
        return 1
    elif k == 0:
        if n == 0:
            return 1
        return 0
    return req(n - 1, k - 1) + k * req(n - 1, k)


def naive(n: int, k: int):
    # if(k > n):
    #     return 0
    # elif(k == n):
    #     return 1
    # elif(k == 0):
    #     if(n == 0):
    #         return 1
    #     return 0
    if k == 1:
        return 1
    s = 0
    for i in range(1, n - k + 2):
        s += binomial(n, i) * naive(n - i, k - 1)
    return s


def get_all(n, k):
    if n == k:
        return [1] * n
    elif k > n:
        return []
    elif n == 0:
        return [], True


def hard(n, k):
    l = get_all(n, k)


# print(req(10, 4))
# print(naive(10, 4) // factorial(4))

for i in range(5):
    print("{" + f"{4}, {i}" + "}" + f"= {req(4, i)}")

print()
print(req(5, 5))
