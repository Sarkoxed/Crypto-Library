# https://math.stackexchange.com/questions/1863037/discrete-logarithm-modulo-powers-of-a-small-prime
# https://www2.eecs.berkeley.edu/Pubs/TechRpts/1984/CSD-84-186.pdf

from sage.all import Zmod, randint, gcd
from tqdm import tqdm


def teta(k, p, s):
    tmp = int(pow(k, (p - 1) * p ** (s - 1), p ** (2 * s - 1)))
    r = ((tmp - 1) // p**s) % p ** (s - 1)
    return r


def dlog(alpha, beta, p, s):
    a = teta(int(alpha), p, s)
    b = teta(int(beta), p, s)
    return (b * pow(a, -1, p ** (s - 1))) % p ** (s - 1)


# 3 - always gen : {-1, 1} union {3^i}
def teta_base2(k, s):
    if k % 4 == 3:
        k = -k
    tmp = pow(k, 2 ** (s - 1), 2 ** (2 * s - 1))
    assert (tmp - 1) % 2 ** (s + 1) == 0
    r = ((tmp - 1) // 2 ** (s + 1)) % 2 ** (s - 2)
    return r


def dlog_base2(alpha, beta, s):
    a = teta_base2(int(alpha), s)
    b = teta_base2(int(beta), s)

    d = gcd(a, 2 ** (s - 2))

    if b % d != 0:
        return None

    a1 = int(a) // d
    b1 = int(b) // d
    c1 = 2 ** (s - 2) // d

    x1 = b1 * pow(a1, -1, c1) % c1
    xs = [x1 + i * c1 for i in range(d)]
    assert all(pow(int(alpha), x, 2**s) == int(beta) for x in xs)
    return xs


def test_p2():
    p = 156210697680525395807405913022225672867518230561026244167727827986872503969390713836672476231008571999805186039701198600755110769232069683662242528076520947841356681828813963095451798586327341737928960287475043247361498716148634925701665205679014796308116597863844787884835055529773239054412184291949429135511
    N = p**2
    a = Zmod(N)(randint(1, N - 1))
    t = randint(1, p - 1)
    b = a**t

    res = dlog(a, b, p, 2)
    a_p = t % p

    assert a_p == res


def test_b2(n=10000):
    s = 64
    for _ in tqdm(range(n)):
        a = Zmod(2**s).random_element()
        while a % 2 == 0:
            a = Zmod(2**s).random_element()

        t = randint(1, 2 ** (s - 1) - 1)
        b = a**t

        res = dlog_base2(a, b, s)
        assert (t % 2 ** (s - 2)) in res


if __name__ == "__main__":
    test_p2()
    test_b2()
