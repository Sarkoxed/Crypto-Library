from factor import factor
from is_prime import is_prime


def quadratic_low(p, q):
    if p == 2:
        return pow(-1, (q**2 - 1) // 8)
    else:
        return pow(-1, (p - 1) * (q - 1) // 4)


def legandre_symbol(p, q, symb=1):
    if p % q == 0:
        return 0
    elif not is_prime(p):
        l = factor(p)
        for primes in l:
            for powers in range(primes[1]):
                symb *= legandre_symbol(primes[0], q)
    else:
        p %= q
        if p != 1:
            symb *= quadratic_low(p, q) * legandre_symbol(q, p)
    return symb
