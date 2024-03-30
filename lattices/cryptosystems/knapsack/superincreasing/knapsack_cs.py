from Crypto.Util.number import *
from knapsack_superincreasing import keygen as kg, decrypt as deq
from random import randint
from math import gcd


def keygen(blocksize, nbit=3):
    r = kg(blocksize, nbit)
    B = randint(2 * r[-1] + 1, 2 * r[-1] + getRandomNbitInteger(nbit))
    A = randint(0, B)
    while gcd(A, B) != 1:
        A = randint(0, B)
    pk = list()
    for i in r:
        pk.append((i * A) % B)
    return ((A, B, r), pk)


def encrypt(m: list, pubkey):
    s = 0
    for i, j in zip(m, pubkey):
        s += i * j
    return s


def decrypt(s, prikey):
    A, B, r = prikey
    s = (pow(A, -1, B) * s) % B

    m = deq(s, r)
    return m
