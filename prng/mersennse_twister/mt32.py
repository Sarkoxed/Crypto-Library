from z3 import BitVec, BitVecVal, Solver, LShR
from random import Random, randint
from tqdm import tqdm

state = [0] * 624
f = 1812433253
m = 397
u = 11
s = 7
b = 0x9D2C5680
t = 15
c = 0xEFC60000
l = 18
index = 624
lower_mask = (1 << 31) - 1
upper_mask = 1 << 31


def twist(state):
    for i in range(624):
        temp = (state[i] & upper_mask) + (state[(i + 1) % 624] & lower_mask)
        temp_shift = temp >> 1
        temp_shift ^= (temp & 1) * 0x9908B0DF % 2**32
        state[i] = state[(i + m) % 624] ^ temp_shift
    return state


def temper(x):
    y = x
    y = y ^ (y >> 11)
    y = y ^ ((y << 7) & 0x9D2C5680)
    y = y ^ ((y << 15) & 0xEFC60000)
    y = y ^ (y >> 18)
    return y


def untemper(out):
    y1 = BitVec("y1", 32)
    y2 = BitVec("y2", 32)
    y3 = BitVec("y3", 32)
    y4 = BitVec("y4", 32)
    y = BitVecVal(out, 32)
    s = Solver()
    equations = [
        y2 == y1 ^ (LShR(y1, 11)),
        y3 == y2 ^ ((y2 << 7) & 0x9D2C5680),
        y4 == y3 ^ ((y3 << 15) & 0xEFC60000),
        y == y4 ^ (LShR(y4, 18)),
    ]
    s.add(equations)
    s.check()
    return s.model()[y1].as_long()


def randbelow(R, x):
    k = x.bit_length()
    r = R.getrandbits(k)
    attempts = 1
    while r >= x:
        attempts += 1
        r = R.getrandbits(k)
    print(f"{attempts=}")
    return r


def randrange(R, x, y=None, step=1):
    if y is None:
        return randbelow(R, x)
    width = y - x
    if step == 1:
        return x + randbelow(R, width)

    n = (width + step - 1) // step
    return x + istep * randbelow(n)


def randint(R, a, b):
    return randrange(R, a, b + 1)


def test_custom():
    R = Random()
    # R.randint(0, 255) // two calls
    R.getrandbits(32)
    state = list(R.getstate()[1][:624])

    s = 17
    for i in tqdm(range(623)):
        assert R.getrandbits(s) == temper(state[1 + i]) >> (32 - s)
    twist(state)
    R.getrandbits(32)
    assert state == list(R.getstate()[1][:-1])


def test_randrange():
    R = Random(1337)
    t1 = randrange(R, 19, 12256)
    R = Random(1337)
    t2 = R.randrange(19, 12256)
    assert t1 == t2


def test_attempts():
    R = Random(1338)
    for i in range(624):
        randbelow(R, 62)


def easy_gen(R, n):
    return [R.getrandbits(6) for _ in range(n)]

def hard_gen(R, n):
    return [R.randint(0, 61) for _ in range(n)]

# test_custom()
# test_randrange()
test_attempts()
