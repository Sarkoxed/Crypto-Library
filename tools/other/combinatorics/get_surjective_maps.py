from sage.all import binomial

# based on the fact that n**d = sum binomial(n, k) * T(d, k) for k in range(1, d+1)


def get_surjective_maps(n, d):
    return sum(binomial(n, k) * (-1) ** (n - k) * k**d for k in range(0, n + 1))


print(get_surjective_maps(5, 5))
