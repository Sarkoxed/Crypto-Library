from math import ceil, floor, log
from Crypto.Util.number import getPrime
from random import randint
from sage.all import crt

def limbs(x, b):
    res = []
    while x:
        res.append(x % 2**b)
        x //= 2**b
    print(res)
    while len(res) < 4:
        res.append(0)
    return res

def partsum(a, b, n):
    res = 0
    for i in range(n + 1):
        res += a[i] * b[n - i]
    return res

def multiplication(a, c, p, n):
    q_w, r_w = divmod(a * c, p)

    t = ceil(log((p**2+p)/n)/log(2))
    assert 2**t * n > p**2
    assert 2**(t-1) * n <= p**2
    assert p.bit_length() < t
    b = t // 4

    q_l = limbs(q_w, b)
    r_l = limbs(r_w, b)
    a_l = limbs(a, b)
    assert len(a_l) == 4
    c_l = limbs(c, b)
    assert len(c_l) == 4

    pp_l = limbs(2**t - p, b)
    
    assert all(x < 2**b for x in q_l + r_l) # well i am honest enough
    
    t0 = partsum(a_l, c_l, 0)  + partsum(q_l, pp_l, 0) 
    assert partsum(a_l, c_l, 0) == a_l[0] * c_l[0]
    assert t0 < 2**(2 * b + 1)
    t1 = partsum(a_l, c_l, 1) + partsum(q_l, pp_l, 1)
    assert t1 < 2**(2 * b + 2)
    t2 = partsum(a_l, c_l, 2) + partsum(q_l, pp_l, 2)
    assert t2 < 6 * 2**(2 * b)
    t3 = partsum(a_l, c_l, 3) + partsum(q_l, pp_l, 3)
    assert t3 < 2**(2 * b + 3)

    u0 = t0 + 2**b * t1 - r_l[0] - r_l[1] * 2**b
    print(bin(u0)[2:], u0.bit_length() - 3 * b)
    assert u0 % 2**(2  * b) == 0

    u1 = t2 + 2**b * t3 - r_l[2] - r_l[3] * 2**b
    print(u1.bit_length() - 3 * b)

    v0 = u0 // 2**(2 * b)
    print(v0.bit_length() - b)

    assert (u1 + v0) % 2**(2 * b) == 0
    v1 = (u1 + v0) // 2**(2 * b)
    print(bin(v1), v1.bit_length() - b)

    assert (a * c - q_w * p - r_w) % n == 0
    assert q_w * p + r_w < 2**t * n

    res = crt([(a * c) % n, (a * c) % 2**t], [n, 2**t]) # yeah well

    print(res)
    print(r_w)

    assert res == r_w


n = getPrime(180)
p = getPrime(256)
a = randint(0, p)
b = randint(0, p)

multiplication(a, b, p, n)
