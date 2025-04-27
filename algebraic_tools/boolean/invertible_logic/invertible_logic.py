from sage.all import GF, Matrix, vector, identity_matrix, ZZ, diagonal_matrix

# 0b bn_1 bn_2 ... b0 
# 0b010101111001011

def i2b(x: int, nbit: int):
    if x.bit_length() > nbit:
        raise ValueError("invalid bit length")
    reslist = ZZ(x).digits(2)
    reslist += [0] * (nbit - len(reslist))
    return vector(GF(2), reslist)

def b2i(v):
    return ZZ(list(v.change_ring(ZZ)), 2)

def shr(sh: int, nbit: int):
    sh %= nbit
    S = Matrix(GF(2), nbit)
    S.set_block(0, sh, identity_matrix(nbit - sh))
    return S

def shl(sh: int, nbit: int):
    sh %= nbit
    S = Matrix(GF(2), nbit)
    S.set_block(sh, 0, identity_matrix(nbit - sh))
    return S

def ror(r: int, nbit: int):
    r %= nbit
    S1 = shr(r, nbit)
    S2 = shl(-r, nbit)
    return S1 + S2

def and_const(x: int, nbit: int):
    return diagonal_matrix(i2b(x, nbit))
