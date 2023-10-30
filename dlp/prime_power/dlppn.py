# https://math.stackexchange.com/questions/1863037/discrete-logarithm-modulo-powers-of-a-small-prime

from sage.all import GF, var, PolynomialRing, Matrix, Zmod, vector, randint

p = 156210697680525395807405913022225672867518230561026244167727827986872503969390713836672476231008571999805186039701198600755110769232069683662242528076520947841356681828813963095451798586327341737928960287475043247361498716148634925701665205679014796308116597863844787884835055529773239054412184291949429135511
N = p ** 2

def teta(k, p, s):
    tmp = int(pow(k, (p-1) * p**(s-1), p**(2 * s - 1)))
    r = ((tmp - 1) // p**s) % p**(s-1)
    return r

def dlog(alpha, beta, p, s):
    a = teta(int(alpha), p, s)
    b = teta(int(beta), p, s)
    return (b * pow(a, -1, p**(s-1))) % p**(s-1)

if __name__ == "__main__":
    a = Zmod(N)(randint(1, N-1))
    r = randint(1, p - 1)
    b = a**r
    
    print(dlog(a, b, p, 2))
    print(r)
