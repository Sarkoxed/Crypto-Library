from sage.all import factor, ZZ, I, floor, sqrt, Integer, is_prime, random_prime, I, divisors, randint

def naive_pairs(n):
    if n == 1:
        return [(0, 1)]
    pairs = []
    for a in range(floor(sqrt(n/2)) + 1):
        b = n - a**2
        if Integer(b).is_square():
            pairs.append((a, int(sqrt(b))))
    return pairs

def naive_count_pairs(n):
    return len(naive_pairs(n))

def naive_pairs_2(n):
    result = []
    for d in divisors(ZZ[I](n)):
        if abs(d * d.conjugate()) == n:
            a, b = abs(d.real()), abs(d.imag())
            a, b = min(a, b), max(a, b)
            if (a, b) not in result:
                result.append((a, b))
    return result

def count_pairs(factors):
    two = None
    primes = []
    if factors[0][0] == 2:
        two = factors[0]
        factors = factors[1:]
    
    Q = 1
    numerator = 1
    for p, a in factors:
        if p % 4 == 3:
            Q *= p**a
        primes.append((p, a))
        numerator *= (a + 1)

    if not Integer(Q).is_square():
        return 0, 0, None

    count = (numerator + 1) // 2 # in case all as are even add 1
    if two is not None:
        primes = [two] + primes

    return count, int(sqrt(Q)), primes

def p4n1(p):
    if p == 2:
        return 1 + I

    c, _ = list(factor(ZZ[I](p)))
    c = c[0]

    a, b = abs(c.real()), abs(c.imag())
    return a + I * b

def all_products(parts):
    if len(parts) == 0:
        return [1]

    res = []
    other_parts = all_products(parts[1:])
    for part in parts[0]:
        res += [part * x for x in other_parts]
        res += [part.conjugate() * x for x in other_parts]
    return res

def pairs(n):
    count, Qsq, primes = count_pairs(list(factor(n)))
    if count == 0:
        return count, []

    parts = []
    
    for p, a in primes:
        lp = p4n1(p)

        uniqs = []
        for i in range((a + 1) // 2):
            uniqs.append(lp**i * lp.conjugate()**(a - i))
        parts.append(uniqs)
    
    u = []
    other_parts = all_products(parts[1:])
    for part in parts[0]:
        u += [part * x for x in other_parts]

    result = []
    for x in u:
        a, b = Qsq * abs(x.real()), Qsq * abs(x.imag())
        a, b = min(a, b), max(a, b)
        if (a, b) not in result: # didn't figure out the smart way to iterate over all the possible products that do not collide
            result.append((a, b))
    return count, result


if __name__ == "__main__":
    from time import time

    while True:
        p = random_prime(10000)
        if p % 4 == 1:
            break
    
    while True:
        q = random_prime(10000)
        if q % 4 == 1:
            break
    
    n = p * q
    n = randint(1, 100000)
    n = 96850
    print(f"Number: {n}")
    print("Gauss approach: ")
    start = time()
    pairs_count, res = pairs(n)
    end = time()
    print(f"Expected: {pairs_count}, got: {len(res)}")
    
    if len(res) == 0:
        print("no decomps")
    else:
        for a,b in res:
            print(f"{a}**2 + {b}**2 = {a**2 + b**2}")
    print(f"Time elapsed: {end - start}")
    
    print("-" * 50)
    start = time()
    res = naive_pairs(n)
    end = time()
    print("Naive approach:")
    print(f"Naive count: {len(res)}")
    if len(res) == 0:
        print("no decomps")
    else:
        for a,b in res:
            print(f"{a}**2 + {b}**2 = {a**2 + b**2}")
    print(f"Time elapsed: {end - start}")
    
    print("-" * 50)
    start = time()
    res = naive_pairs_2(n)
    end = time()
 
    print("Naive approach 2:")
    print(f"Naive count: {len(res)}")
    if len(res) == 0:
        print("no decomps")
    else:
        for a,b in res:
            print(f"{a}**2 + {b}**2 = {a**2 + b**2}")
    print(f"Time elapsed: {end - start}")
