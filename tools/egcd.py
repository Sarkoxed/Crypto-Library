def extended_euclides(a,b,quo=lambda a,b:a//b):
    r0 = a; r1 = b
    s0 = 1; s1 = 0
    t0 = 0; t1 = 1

    while r1 != 0:
        q = quo(r0, r1)
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
        t0, t1 = t1, t0 - q * t1

    return r0, s0, t0
    
def extra(ass):
    coeffs = []
    a, b = ass[:2]
    d, c1, c2 = extended_euclides(a, b)
    coeffs += [c1, c2]
    print(gcd(a, b), c1 * a + c2 * b)
    for i in range(2, len(ass)):
        a = d
        b = ass[i]
        d, c1, c2 = extended_euclides(a, b)
        for j in range(len(coeffs)):
            coeffs[j] *= c1
        coeffs.append(c2)
    return coeffs
