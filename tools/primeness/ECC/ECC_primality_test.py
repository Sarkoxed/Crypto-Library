from sage.all import EllipticCurve, Zmod, sqrt, ceil, ZZ, Primes
from order.curve_order import get_nullifier

def is_prime(n, m = 100):
    G = Zmod(n)
    bound = ceil(ZZ(n)**(1/4) + 1)**2
    
    ps = []
    prod = 1
    for p in Primes():
        if p == 2:
            continue
        prod *= p
        ps.append(p)
        if prod > bound:
            break
    ps0 = ps.copy()
    print(ps)

    for _ in range(m):
        a, b, A = [G.random_element() for _ in range(3)]
        B = b**2 - a**3 - a * A
        e = EllipticCurve(G, [A, B])
        P = e((a, b))
        
        try:
            M = get_nullifier(P)
        except ZeroDivisionError:
            return False
        # didn't find an integer => the order is greater than for prime
        except ValueError: 
            return False

        for p in ps:
            if M % p != 0:
                continue
            M1 = M
            while M1 % p == 0:
                M1 //= p
            if M1 * P == 0:
                continue
            ps.remove(p)

        if len(ps) == 0:
            return True

    return ps0, ps

if __name__ == "__main__":
    print(is_prime(82020246603121261))
    print(is_prime(672486484325791283))
