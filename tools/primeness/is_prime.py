from math import sqrt


def is_prime(n):
    if n == 1:
        return False
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False
    return all([n % x != 0 for x in range(3, int(sqrt(n)) + 1, 2)])


def is_prime_2(n):
    return is_prime(n)
