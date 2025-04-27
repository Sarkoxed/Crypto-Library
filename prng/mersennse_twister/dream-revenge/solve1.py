from z3 import BitVec, BitVecVal, Solver, LShR
import random

state = [0]*624
f = 1812433253
m = 397
u = 11
s = 7
b = 0x9D2C5680
t = 15
c = 0xEFC60000
l = 18
index = 624
lower_mask = (1 << 31)-1
upper_mask = 1 << 31

def twist(state):
    for i in range(624):
        temp = (state[i] & upper_mask) + (state[(i + 1) % 624] & lower_mask)
        temp_shift = LShR(temp, 1)
        temp_shift ^= (temp & 1) * 0x9908b0df
        state[i] = state[(i + m) % 624] ^ temp_shift
    return state


def untemper(out):
    """
    This is the untemper function, i.e., the inverse of temper. This
    is solved automatically using the SMT solver Z3. I could prpbably
    do it by hand, but there is a certain elegance in untempering symbolically.
    """
    y1 = BitVec('y1', 32)
    y2 = BitVec('y2', 32)
    y3 = BitVec('y3', 32)
    y4 = BitVec('y4', 32)
    y = BitVecVal(out, 32)
    s = Solver()
    equations = [
        y2 == y1 ^ (LShR(y1, 11)),
        y3 == y2 ^ ((y2 << 7) & 0x9D2C5680),
        y4 == y3 ^ ((y3 << 15) & 0xEFC60000),
        y == y4 ^ (LShR(y4, 18))
    ]
    s.add(equations)
    s.check()
    return s.model()[y1].as_long()

known = [random.getrandbits(32) for _ in range(624)]

s1 = untemper(known[1])
s2 = untemper(known[2])
s3 = untemper(known[3])
s4 = untemper(known[4])

assert s1 == random.getstate()[1][1]
assert s2 == random.getstate()[1][2]
assert s3 == random.getstate()[1][3]
assert s4 == random.getstate()[1][4]

s387 = untemper(known[397])
s388 = untemper(known[398])
s389 = untemper(known[399])
s390 = untemper(known[400])

assert s387 == random.getstate()[1][397]
assert s388 == random.getstate()[1][398]
assert s389 == random.getstate()[1][399]
assert s390 == random.getstate()[1][400]


def find_next(s0, s1, s2):
    temp = (s0 & upper_mask) + (s1 & lower_mask)
    temp_shift = temp >> 1
    temp_shift ^= (temp & 1) * 0x9908b0df
    return s2 ^ temp_shift

s0_1 = find_next(1 << 31, s1, s387)
s0_10 = find_next(0, s1, s387)

s0_2 = find_next(s1, s2, s388)
s0_3 = find_next(s2, s3, s389)
s0_4 = find_next(s3, s4, s390)

def temper(in_value):
    y = in_value
    y = y ^ (y >> u)
    y = y ^ ((y << s) & b)
    y = y ^ ((y << t) & c)
    y = y ^ (y >> l)
    return y


print(temper(s0_1) +  temper(s0_2) * 2**32 + temper(s0_3) * 2**64 + temper(s0_4) * 2**96)
print(temper(s0_10) + temper(s0_2) * 2**32 + temper(s0_3) * 2**64 + temper(s0_4) * 2**96)

print(random.getrandbits(128))

sh1 = (s1 & lower_mask)
print((sh1 >> 1) ^ ((sh1 & 1) * 0x9908b0df) ^ s387,  random.getstate()[1][0])
sh1 = (s1 & upper_mask) | (s2 & lower_mask)
print((sh1 >> 1) ^ ((sh1 & 1) * 0x9908b0df) ^ s388,  random.getstate()[1][1])

sh1 = (s1 & upper_mask) | (s2 & lower_mask)
print((sh1 >> 1) ^ ((sh1 & 1) * 0x9908b0df) ^ s388,  random.getstate()[1][1])
