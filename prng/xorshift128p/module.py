#!/usr/bin/python3
import z3
import struct
import sys
from math import floor

def solve(sequence):
    sequence = sequence[::-1]
    solver = z3.Solver()
    se_state0, se_state1 = z3.BitVecs("se_state0 se_state1", 64)
    se_st0, se_st1 = z3.BitVecs("se_st0 se_st1", 64)
    solver.add(se_st1 == se_state1)
    solver.add(se_st0 == se_state0)

    for i in range(len(sequence)):
        se_s1 = se_state0
        se_s0 = se_state1
        se_state0 = se_s0
        se_s1 ^= se_s1 << 23
        se_s1 ^= z3.LShR(se_s1, 17)  # Logical shift instead of Arthmetric shift
        se_s1 ^= se_s0
        se_s1 ^= z3.LShR(se_s0, 26)
        se_state1 = se_s1

        tmp = z3.LShR(se_state0, 12) + 2**52
        tmp = z3.LShR(tmp, 52 - 2)
        solver.add(tmp == sequence[i] + 4)

    while solver.check() == z3.sat:
        model = solver.model()
        states = {}
        for state in model.decls():
            states[state.__str__()] = model[state]

        print(states)
        state0 = states["se_state0"].as_long()
        state1 = states["se_state1"].as_long()
        if state0 == 6841556592272590657:
            print("PIZDA")
            exit()

        solver.add(z3.And(se_st0 != state0, se_st1 != state1))
        u_long_long_64 = (state0 >> 12) | 0x3FF0000000000000
        float_64 = struct.pack("<Q", u_long_long_64)
        next_sequence = struct.unpack("d", float_64)[0]
        next_sequence -= 1

        out = floor(4 * next_sequence)
        print(out)
        
        #alphabet = '☊☋☌☍'
        #cur = ''
        #out = [x for x in sequence][::-1]
        #for i in range(10):
        #    cur +=  alphabet[floor(next_sequence * 4)]                               
        #    next_sequence = get_next([x for in out[-6:] + [next_sequence]])
        #    out.append(next_sequencce)

        
from inp import sequence
seq0 = []
for i in range(0, len(sequence), 64):
    if len(sequence[i: i + 64]) < 64:
        break
    seq0.extend(sequence[i: i + 64][::-1])
seq = seq0[::-1]

n = int(input("n: "))
seq = [floor(4 * x) for x in seq[-n:]]
solve(seq)
