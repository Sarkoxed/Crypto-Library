from Crypto.Util.number import getPrime, long_to_bytes, bytes_to_long
from random import randint
from os import urandom
from gmpy2 import mpq


def pkcs1(m, n):
    k = len(long_to_bytes(n))

    if len(m) > k - 11:
        raise ValueError(f"lol n = {n}, k ={k}, m = {m}, len(m) = {m}")
    p = k - 3 - len(m)
    while True:
        pad = urandom(p)
        if b"\x00" not in pad:
            break
    return b"\x00\x02" + pad + b"\x00" + m

def unpkcs1(m, n):
    k = len(long_to_bytes(n))

    if len(m) != k - 1:
        raise ValueError("Wrong padding")
    ind = m.index(b'\x00')
    m = m[ind + 1:]
    return m

def valid_pkcs(c):
    k = len(long_to_bytes(n))
    r = pow(c, d, n)
    r = b"\x00" + long_to_bytes(r)
    if len(r) != k:
        return False
    if r[1] != 2:
        return False
    return True

def attack(c, e, n):
    k = -(-n.bit_length() // 8)
    B = 2**(8 * (k - 2))
