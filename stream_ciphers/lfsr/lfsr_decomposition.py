from sage.all import PolynomialRing, GF, Matrix, var, vector

def get_matrix(qs):
    m = len(qs) - 1
    return Matrix([qs[:j+1][::-1] + [0 for _ in range(m-j-1)] for j in range(m)])

def recover_states(GF):
    states = []
    polys = []
    for Gfi in Gf.partial_fraction_decomposition()[1]:
        num, den = Gfi.numerator(), Gfi.denominator()
        qtmp = list(den)
        mtmp = get_matrix(qtmp)
        numlist = list(num)
        for _ in range(len(numlist), den.degree()):
            numlist.append(0)
    
        state = mtmp**-1 * vector(numlist)
        states.append(list(state))
        polys.append(list(den)[1:][::-1])
    return states, polys

def get_lfsr_seqs(states, polys, length):
    patterns = []
    for i in range(len(polys)):
        state, poly = [x for x in states[i]], polys[i]
        for i in range(length - len(state)):
            tmp1 = sum(x * y for x, y in zip(poly, state[i:i+len(poly)])) % 2 # lfsr step
            state.append(tmp1)
        patterns.append(state)

    return patterns

x = var('x')
f = PolynomialRing(GF(2), x)
s = [0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 
0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 
 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0 
, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1]
modpoly = f(1 + x + x**(128 -96) + x**(128 - 64) + x**(128 - 32) + x**(128 - 16) + x**(128))


qs = list(modpoly)
numerator = f(list(get_matrix(qs) * vector(s)))
Gf = numerator / modpoly

states, polys = recover_states(Gf)
patterns = get_lfsr_seqs(states, polys, len(s))

assert [sum(patterns[i][j] for i in range(len(states))) % 2 for j in range(128)] == s
