# crypto.standford.edu/pbc/notes/ep/tonelli.html

from sage.all import *


def tonelli_sqrt(a, p):
    g = 2
    while pow(g, (p - 1) // 2, p) != 1:
        g = randint(1, p - 1)
    
    s, t = 0, p - 1
    while t % 2 == 0:
        t //= 2
        s += 1

    if s == 1:
        return pow(a, (p + 1) // 4, p)
    
    e = 0
    for i in range(2, s + 1):
        if pow(a * pow(g, -e, p), (p - 1) // pow(2, i)) != 1:
            e = pow(2, i - 1) + e

    h = a * pow(g, -e, p) % p
    b = pow(g, e // 2, p) * pow(h, (t + 1) // 2, p) % p
    return b

def tonelli_sqrt1(a, p):
    assert pow(a, (p - 1) // 2, p) == 1, "a is not a quadratic residue modulo p"
    
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    
    s = 0
    q = p - 1
    while q % 2 == 0:
        q //= 2
        s += 1

    z = 2
    while pow(z, (p - 1) // 2, p) == 1:
        z = randint(1, p - 1)
    
    c = pow(z, q, p)
    r = pow(a, (q + 1) // 2, p)
    t = pow(a, q, p)
    m = s
    
    while t != 1:
        i = 0
        temp = t
        while temp != 1:
            temp = pow(temp, 2, p)
            i += 1
        b = pow(c, 2**(m - i - 1), p)
        r = (r * b) % p
        t = (t * b * b) % p
        c = (b * b) % p
        m = i

    return r


p = random_prime(10000000)
a = randint(1, p - 1)
while pow(a, (p - 1) // 2, p) != 1:
    a = randint(1, p - 1)

b = tonelli_sqrt1(a, p)
print(f"{p % 4}")
assert pow(b, 2, p) == a
print(f"{p, a, b=}")
