from Crypto.Util.number import getPrime
from sage.all import GF, EllipticCurve, Zmod, lcm


def setup(nbit):
    p = getPrime(nbit)
    while p % 3 != 2:
        p = getPrime(nbit)
    q = getPrime(nbit)
    while q % 3 != 2:
        q = getPrime(nbit)

    e = 0x10001
    d = pow(e, -1, lcm(p + 1, q + 1))
    n = p * q
    return (e, n), (d, p, q)


def encrypt(pkey, msg):
    e, n = pkey
    msg = msg + len(msg).to_bytes(4, "big")
    M = len(msg)
    m1, m2 = int.from_bytes(msg[: M // 2], "big"), int.from_bytes(msg[M // 2 :], "big")
    b = (m2**2 - m1**3) % n

    E = EllipticCurve(Zmod(n), [0, b])
    C = e * E((m1, m2))
    return C


def decrypt(skey, C):
    d, _, _ = skey
    M = d * C

    mlen = int(M[1]) % 2**32 + 4
    m1 = int(M[0]).to_bytes(mlen // 2, "big")
    m2 = int(M[1]).to_bytes(mlen // 2, "big")[:-4]
    return m1 + m2


pkey, skey = setup(256)
M = b"Hey, Bub. What's up?"

C = encrypt(pkey, M)
msg = decrypt(skey, C)

print(msg)
