def murmur(x):
    x ^= x >> 33
    x = (x * 0xFF51AFD7ED558CCD) % 2**64
    x ^= x >> 33
    x = (x * 0xC4CEB9FE1A85EC53) % 2**64
    x ^= x >> 33
    return x

import z3

def se_murmur(x):
    x ^= z3.LShR(x, 33)
    x = (x * 0xFF51AFD7ED558CCD) % 2**64
    x ^= z3.LShR(x, 33)
    x = (x * 0xC4CEB9FE1A85EC53)
    x ^= z3.LShR(x, 33)
    return x


def state_to_seed(st0, st1):
    v4 = z3.BitVec("v4", 64)
    v5 = se_murmur(v4)
    v6 = se_murmur(v4 ^ (2**64 - 1))
    s = z3.Solver()
    s.add(v5 == st0)
    s.add(v6 == st1)
    if s.check() == z3.sat:
        m = s.model()
        s.add(v4 != m[v4])
        assert s.check() == z3.unsat
        return m[v4].as_long()
