from sage.all import GF, Matrix, vector, identity_matrix, ZZ, diagonal_matrix
from invertible_logic import i2b, b2i, shl, shr, ror, and_const
from random import getrandbits, seed
from tqdm import tqdm

def test():
    nbit = 64
    shift = 17

    a = getrandbits(nbit)
    t1 = b2i(shr(shift, nbit) * i2b(a, nbit))
    t2 = a >> shift
    assert t1 == t2

    a = getrandbits(nbit)
    t1 = b2i(shl(shift, nbit) * i2b(a, nbit))
    t2 = (a << shift) % 2**nbit
    assert t1 == t2

    a = getrandbits(nbit)
    t1 = b2i(ror(shift, nbit) * i2b(a, nbit))
    t2 = ((a >> shift) | (a << (nbit - shift))) % 2**nbit
    assert t1 == t2

    
    a = getrandbits(nbit)
    b = getrandbits(nbit)
    t1 = b2i(and_const(b, nbit) * i2b(a, nbit))
    t2 = a & b
    assert t1 == t2

def test_temper_mt32():
    def temper(x):
        y = x
        y = y ^ (y >> 11)
        y = y ^ ((y << 7) & 0x9D2C5680)
        y = y ^ ((y << 15) & 0xEFC60000)
        y = y ^ (y >> 18)
        return y

    def mtemper():
        y = identity_matrix(GF(2), 32)
        y = y + shr(11, 32) * y
        y = y + and_const(0x9D2C5680, 32) * shl(7, 32) * y
        y = y + and_const(0xEFC60000, 32) * shl(15, 32) * y
        y = y + shr(18, 32) * y
        return y
    x = getrandbits(32)

    y1 = temper(x)
    y2 = b2i(mtemper() * i2b(x, 32))
    assert y1 == y2

test()
test_temper_mt32()

def play_with_temper():
    def mtemper():
        y = identity_matrix(GF(2), 32)
        y = y + shr(11, 32) * y
        y = y + and_const(0x9D2C5680, 32) * shl(7, 32) * y
        y = y + and_const(0xEFC60000, 32) * shl(15, 32) * y
        y = y + shr(18, 32) * y
        return y

    T = mtemper()
    print(T)
    print(T.det())

def test_xor_shr(n):
    for i in tqdm(range(1, n)):
        for j in range(10000):
            a = getrandbits(n)
            b = a ^ (a >> i)
            c = 0
            for j in range(0, n, i):
                c ^= b >> j
            assert a == c
test_xor_shr(32)

def test_xor_shl(n):
    m = 2**n
    for i in tqdm(range(1, n)):
        for j in range(10000):
            a = getrandbits(n)
            b = a ^ ((a << i) % m)
            c = 0
            for j in range(0, n, i):
                c ^= (b << j) % m
            assert a == c
test_xor_shl(32)

def test_xor_shift(i):
    S = identity_matrix(16) + shr(i, 16)
    print(S)
    print(S.det())
    print(S**-1)
#test_xor_shift(3)

a = getrandbits(16)
b = a ^ (a >> 2)
c = b ^ (b >> 2) 
