import struct
from math import floor

def check_mod(se_state0, se_state1, sequence):
    sequence = sequence[::-1]
    for i in range(len(sequence)):
        se_s1 = se_state0
        se_s0 = se_state1
        se_state0 = se_s0
        se_s1 ^= (se_s1 << 23) % 2**64
        se_s1 ^= se_s1 >> 17  # Logical shift instead of Arthmetric shift
        se_s1 ^= se_s0
        se_s1 ^= se_s0 >> 26
        se_state1 = se_s1

        tmp = (se_state0 >> 12) + 2**52
        tmp = tmp >> (52 - 2)

        tmp1 = (se_state0 >> 12) | 0x4010000000000000 # just checking
        float_64 = struct.pack("<Q", tmp1)
        tmp2 = struct.unpack("d", float_64)[0]

        u_long_long_64 = (se_state0 >> 12) | 0x3FF0000000000000
        float_64 = struct.pack("<Q", u_long_long_64)
        next_sequence = struct.unpack("d", float_64)[0]
        #print(tmp2)
        #print(next_sequence * 4)
        next_sequence -= 1

        #print(tmp)
        assert tmp == sequence[i] + 4

def check(se_state0, se_state1, sequence):
    sequence = sequence[::-1]
    for i in range(len(sequence)):
        se_s1 = se_state0
        se_s0 = se_state1
        se_state0 = se_s0
        se_s1 ^= (se_s1 << 23) % 2**64
        se_s1 ^= se_s1 >> 17  # Logical shift instead of Arthmetric shift
        se_s1 ^= se_s0
        se_s1 ^= se_s0 >> 26
        se_state1 = se_s1

        u_long_long_64 = (se_state0 >> 12) | 0x3FF0000000000000
        float_64 = struct.pack("<Q", u_long_long_64)
        next_sequence = struct.unpack("d", float_64)[0]
        next_sequence -= 1
        assert next_sequence == sequence[i], f"{i}"


def get_next(state0, state1):
    u_long_long_64 = (state0 >> 12) | 0x3FF0000000000000
    float_64 = struct.pack("<Q", u_long_long_64)
    next_sequence = struct.unpack("d", float_64)[0]
    next_sequence -= 1

    s1 = state0
    s0 = state1
    state0 = s0
    s1 ^= (s1 << 23) % 2**64
    s1 ^= s1 >> 17  # Logical shift instead of Arthmetric shift
    s1 ^= s0
    s1 ^= s0 >> 26
    state1 = s1

    return state0, state1, next_sequence

if __name__ == "__main__":
    from inp import state0, state1, sequence
    seq0 = []
    for i in range(0, len(sequence), 64):
        if len(sequence[i: i + 64]) < 64:
            break
        seq0.extend(sequence[i: i + 64][::-1])

    seq = seq0[::-1]

    check(state0, state1, seq)
    seq1 = [floor(4 * x) for x in seq]
    check_mod(state0, state1, seq1)
