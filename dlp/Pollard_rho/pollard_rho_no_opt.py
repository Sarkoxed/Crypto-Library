from Crypto.Util.number import getPrime
from sage.all import GF, Zmod, floor, gcd, log, randint, random_prime


def getPowers1(a, x, g, h, p, k=1):
    ax, bx = a

    if x not in GF(p):
        par = sum(int(x) * p**i for i, x in enumerate(list(x)))

        r = len(list(x))
        lb = p ** (r - 1)
        step = (p**r - lb) // 3
    else:
        lb = 0
        step = p // 3
        par = int(x)

    if par >= lb and par < lb + step:
        ax += 1
        x *= g
    elif par >= lb + step and par < lb + 2 * step:
        ax *= 2
        bx *= 2
        x = x**2
    else:
        bx += 1
        x *= h

    return (ax, bx), x


# performs slightly better, according to benchmarks
def getPowers2(a, x, g, h, p, k=1):
    ax, bx = a

    N = p**k
    if x not in GF(p):
        par = sum(int(x) * p**i for i, x in enumerate(list(x)))
    else:
        par = int(x)

    if par < N // 3:
        ax += 1
        x *= g
    elif par >= N // 3 and par < 2 * N // 3:
        ax *= 2
        bx *= 2
        x = x**2
    else:
        bx += 1
        x *= h

    return (ax, bx), x


def pollard_rho(g, h, p, k=1):
    N = g.multiplicative_order()
    Pm = Zmod(N)

    ex = (Pm(0), Pm(0))
    ey = (Pm(0), Pm(0))

    G = GF(p**k)
    x, y = G(1), G(1)
    while True:
        ex, x = getPowers(ex, x, g, h, p, k)

        ey, y = getPowers(ey, y, g, h, p, k)
        ey, y = getPowers(ey, y, g, h, p, k)

        if x == y:
            break

    u = int(ex[0] - ey[0])
    v = int(ey[1] - ex[1])
    d = gcd(v, N)
    assert u % d == 0

    u //= d
    N //= d
    v //= d

    res = Pm(pow(v, -1, N) * u)
    dlp = []
    for k in range(d):
        dlp.append(res + k * N)

    return dlp


getPowers = getPowers2


def test(n=1, nbit=20):
    from time import time

    k = nbit // n
    p = getPrime(k)
    G = GF(p**n)

    g = G.random_element()
    x = randint(1, p - 1)
    h = g**x

    start = time()
    pos = pollard_rho(g, h, p, n)
    end = time()
    assert x in pos
    return end - start


if __name__ == "__main__":
    t = 0.0
    m = 20
    for _ in range(m):
        t += test(n=3, nbit=30)
        print(f"CurrentAvg: {t / (_ + 1)}")
    print(f"AvgTime: {t / m}")
