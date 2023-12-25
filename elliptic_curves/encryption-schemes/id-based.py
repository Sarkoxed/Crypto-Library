from Crypto.Hash import BLAKE2b
from Crypto.Util.number import getPrime, isPrime
from sage.all import GF, ZZ, EllipticCurve, randint


def setup(nbit, mbit=128):
    p = getPrime(nbit - 1)
    q = 6 * p - 1
    while not (isPrime(q) and q % 3 == 2):
        p = getPrime(nbit - 1)
        q = 6 * p - 1

    E = EllipticCurve(GF(q), [0, 1])
    P = E.gens()[0] * 6
    assert P.order() == p
    s = randint(1, p - 1)
    return (E, P, s * P, p, mbit), s


def H1(E, m, nbit=128, padbit=7):
    H = BLAKE2b.new(data=m, digest_bits=nbit)
    y_m = int.from_bytes(H.digest(), "big")
    
    q = E.base_ring().order()
    G = GF(q)
    
    d1 = pow(3, -1, q - 1)
    x_m = (G(y_m)**2 - 1)**d1
    return E((x_m, ZZ(y_m))) * 6


def H2(t, n):
    a, b = list(t)
    H = BLAKE2b.new(data=f"{a}||{b}".encode(), digest_bits=n)
    return H.digest()


def pairing(P, Q, l):
    q = P.base_ring().order()
    G2 = GF(q**2)
    w = G2(1).nth_root(3, all=True)[1]
    E1 = EllipticCurve(G2, [0, 1])
    Q = E1((Q[0] * w, Q[1]))
    assert P * l == 0
    assert Q * l == 0
    return P.change_ring(G2).weil_pairing(Q, l)


def get_private_key(pub, s, id, nbit=128, padbit=7):
    Q_id = H1(pub[0], id, nbit, padbit)
    D_id = s * Q_id
    return Q_id, D_id


def encrypt(pub, msg, dest_id, nbit=128, padbit=7):
    E, P, Ppub, l, mbit = pub
    B_id = H1(E, id_bob, nbit, padbit)
    r = randint(1, l - 1)
    g_id = pairing(B_id, Ppub, l)
    c0 = r * P
    c1 = bytes([x ^ y for x, y in zip(msg, H2(g_id**r, mbit))])
    return (c0, c1)


def decrypt(pub, D_id, C):
    _, _, _, l, mbit = pub
    c0, c1 = C

    h_id = pairing(D_id, c0, l)
    m = bytes([x ^ y for x, y in zip(c1, H2(h_id, mbit))])
    return m


pub, s = setup(nbit=128, mbit=256)
id = b"vergil@power.com"

id_bob = b"dante@pizza.com"
msg = b"I need more power, brother"
C = encrypt(pub, msg, id_bob)


B_id, BD_id = get_private_key(pub, s, id_bob)
m = decrypt(pub, BD_id, C)
print(m)
