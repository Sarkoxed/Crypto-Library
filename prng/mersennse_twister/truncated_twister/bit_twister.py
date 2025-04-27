#from sage.all import Matrix, GF, PolynomialRing
from random import Random
from tqdm import tqdm
from z3 import Solver, BitVec, sat
from time import time

def shl(x, n):
    return x[n:] + [0] * n

def shr(x, n):
    return [0] * n + x[:-n]

def xor(a, b):
    return [x ^ y for x, y in zip(a, b)]

def and_(a, b):
    return [x if y == 1 else 0 for x, y in zip(a, b)]

def i2b(a):
    return [int(x) for x in bin(a)[2:].zfill(32)]

def b2i(b):
    return sum(int(b[31 - i]) * 2**i for i in range(32))

def twist(state):
    b = i2b(0x9908B0DF)
 
    for i in range(624):
        temp = state[i][:1] + state[(i + 1) % 624][1:]
        temp_shift = [0] + temp[:-1]
        x0 = temp[-1]
        for j in range(32):
            add = x0 if b[j] == 1 else 0
            temp_shift[j] ^= add
        state[i] = xor(state[(i + 397) % 624], temp_shift)

def temper(x):
    y = x.copy()
    y = xor(y, shr(y, 11))
    y = xor(y, and_(shl(y, 7), i2b(0x9D2C5680)))
    y = xor(y, and_(shl(y, 15), i2b(0xEFC60000)))
    y = xor(y, shr(y, 18))
    return y

def test_custom():
    R = Random()
    # R.randint(0, 255) // two calls
    R.getrandbits(32)
    state = list(R.getstate()[1][:624])
    state_bin = [i2b(y) for y in state]

    s = 17
    for i in range(623):
        assert R.getrandbits(s) == b2i(temper(state_bin[1 + i])) >> (32 - s)
    twist(state_bin)
    R.getrandbits(32)
    assert [b2i(x) for x in state_bin] == list(R.getstate()[1][:-1])

R = Random(1337)
def easy_gen(R, n, m=6):
    res = [R.getrandbits(m)]
    st0 = R.getstate()[1][:-1]
    return res + [R.getrandbits(m) for _ in range(n - 1)], st0

m = 6
out, st0 = easy_gen(R, (624 * 32 + m - 1) // m, m)

S = Solver()

gens = [BitVec(f"s_{i}", 1) for i in range(624 * 32)]
s_state = [gens[i:i+32] for i in range(0, 624 * 32, 32)]
f_state = s_state.copy()

outs = []
k = len(out)
for i in tqdm(range(k)):
    if i != 0 and i % 624 == 0:
        twist(s_state)
    outi = i2b(out[i])[-m:]
    out_s = temper(s_state[i % 624])[:m]
    for j in range(m):
        S.add(out_s[j] == outi[j])

start = time()
res = S.check()
print(res)
end = time()
print(f"time: {end - start}")

Z = 12
if res == sat:
    m = S.model()
    recovered_state = [[S.model()[x] for x in st] for st in f_state]
    for i in range(Z):
        t1 = [S.model()[x] for x in f_state[i]]
        t2 = i2b(st0[i])
        if any(x is not None for x in t1):
            t1 = [int(str(x)) for x in t1]
            print(b2i(t1) == b2i(t2))
