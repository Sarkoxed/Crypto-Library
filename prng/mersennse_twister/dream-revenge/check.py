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


s = Solver()

known = [random.getrandbits(32) for _ in range(624)]

state = [BitVec(f"s_{i}", 32) for i in range(624)]
res_state = [BitVec("ss1", 32),
BitVec("ss2", 32),
BitVec("ss3", 32),
BitVec("ss4", 32),
BitVec("ss5", 32),
BitVec("ss6", 32),
BitVec("ss7", 32),
BitVec("ss8", 32)]

s.add(state[1] == untemper(known[1]))
s.add(state[2] == untemper(known[2]))
s.add(state[3] == untemper(known[3]))
s.add(state[4] == untemper(known[4]))
s.add(state[387] == untemper(known[387]))
s.add(state[388] == untemper(known[388]))
s.add(state[389] == untemper(known[389]))
s.add(state[390] == untemper(known[390]))

state1 = twist(state.copy())
for i in range(8):
    s.add(res_state[i] == state1[i])

for i in range(8):
    print(random.getrandbits(32))

print(s.check())
for rs in res_state:
    print(s.model()[rs])
#for s1 in state:
#    print(s.model()[s1])
