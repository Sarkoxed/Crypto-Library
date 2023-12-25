from os import urandom

from Crypto.Cipher import AES
from Crypto.Hash import BLAKE2b
from Crypto.Util.number import getPrime
from Crypto.Util.Padding import pad, unpad
from sage.all import GF, EllipticCurve, randint


def setup(nbit):
    p = getPrime(nbit)
    a, b = 1, 2
    E = EllipticCurve(GF(p), [a, b])
    N = E.order()
    A = E.random_point()
    s = randint(1, N - 1)
    B = s * A
    return (E, A, B, p), s


def encrypt(pkey, msg):
    E, A, B, p = pkey
    N = E.order()
    k = randint(1, N - 1)
    R = k * A
    Z = k * B

    H1 = BLAKE2b.new(digest_bytes=32)
    H1.update(f"{R.xy()}||{Z.xy()}".encode())
    k1k2 = H1.digest()

    k1, k2 = k1k2[:16], k1k2[16:]

    iv = urandom(16)
    C = AES.new(k1, mode=AES.MODE_CBC, iv=iv)
    ct = iv + C.encrypt(pad(msg, 16))

    H2 = BLAKE2b.new(digest_bytes=16)
    H2.update(ct + b"||" + k2)
    t = H2.digest()
    return (R, ct, t)


def decrypt(pkey, skey, C):
    R, ct, t = C
    E, A, B, p = pkey

    Z = skey * R
    H1 = BLAKE2b.new(digest_bytes=32)
    H1.update(f"{R.xy()}||{Z.xy()}".encode())
    k1k2 = H1.digest()

    k1, k2 = k1k2[:16], k1k2[16:]

    H2 = BLAKE2b.new(digest_bytes=16)
    H2.update(ct + b"||" + k2)
    t_ = H2.digest()
    if t_ != t:
        return None

    iv, ct = ct[:16], ct[16:]
    D = AES.new(k1, mode=AES.MODE_CBC, iv=iv)
    msg = unpad(D.decrypt(ct), 16)
    return msg


pkey, skey = setup(128)
C = encrypt(pkey, b"Hey Bubs")
M = decrypt(pkey, skey, C)
print(M)
