from sage.all import EllipticCurve, sqrt, gcd, GF, ZZ
from Crypto.Util.number import getPrime, isPrime, getRandomNBitInteger

# N = p^n + 1 - a
def check_existance(N, p, n, a):
    if abs(a)**2 >= 4 * p**n:
        return False

    if (N % 2 == 0 and abs(a) == 2 * sqrt(p**n)):
        return 1

    if (N % 2 == 0 and p % 3 != 1 and abs(a) == sqrt(p**n)):
        return 2

    if (N % 2 == 1 and p in [ 2, 3 ] and abs(a) == p):
        return 3

    if (N % 2 == 0 and p % 4 != 1 and a == 0):
        return 4

    if (N % 2 == 1 and a == 0):
        return 5

    if gcd(a, p) == 1:
        return 0

    return None

# N = p^e * n1 * n2, n1 | n2, p !| n1, n1 can be 1 E(F_q) ~ Zp^e x Zn1 x Zn2
def check_existance_decomposition(p, e, n1, n2, n, a):
    N = p**e * n1 * n2
    t = check_existance(N, p, n, a)
    if t is None:
        return False

    if t == 2:
        return n1 == n2
    
    return (q - 1) % n1 == 0


def get_square_order(nbit):
    n = ZZ(getRandomNBitInteger(nbit))
    
    q1 = n**2 + 1
    q2 = n**2 + n + 1
    q3 = n**2 - n + 1
    q4 = (n + 1)**2
    q5 = (n - 1)**2
    
    for q in [q1, q2, q3, q4, q5]:
        if q.is_prime_power():
            g = GF(q)
            while True:
                a = g.random_element()
                b = g.random_element()
                e = EllipticCurve(g, [a, b])
                if e.order().is_square():
                    return a, b, q
print(get_square_order(10))
