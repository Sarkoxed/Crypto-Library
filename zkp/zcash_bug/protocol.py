from py_ecc.bn128 import G1, G2, add, multiply, pairing
from py_ecc.bn128 import curve_order as q
from sage.all import GF, Matrix, PolynomialRing, var

from gen_srs import srs

# q - 1 =  2^28 * 3^2 * 13 * 29 * 983 * 11003 * 237073 * 405928799 * 1670836401704629 * 13818364434197438864469338081

x = var("x")
P = PolynomialRing(GF(q), x)

E1 = multiply(G1, 0)
E2 = multiply(G2, 0)

def fundamental_domain(n_points):
    return range(n_points)
    # g = GF(q).multiplicative_generator()**(p-)
    # return [pow(g, i) for i in range(m)]


def column_to_poly(column, domain):
    return P.lagrange_polynomial(
        zip(domain, column)
    )  # can be done efficient using ffts, but I won't


def matrix_to_polys(A, witness, domain):
    _, m = A.dimensions()

    res = 0
    for i in range(m):
        res += witness[i] * column_to_poly(A.T[i], domain)
    return res


def Quotient(poly, domain):
    Z = 1
    for w in domain:
        Z *= P(x - w)
    assert poly % Z == 0
    return Z, poly // Z


def commit(poly, flag: bool):
    powers = srs[flag]
    comm = [E1, E2][flag]

    for i, coeff in enumerate(poly):
        comm = add(comm, multiply(powers[i], int(coeff)))
    return comm


def prove(A, B, C, witness, mpub):
    n, m = A.dimensions()
    domain = fundamental_domain(n)

    Ax = matrix_to_polys(A, witness, domain)
    Bx = matrix_to_polys(B, witness, domain)
    Cx = matrix_to_polys(C, witness, domain)

    Lx = Ax * Bx - Cx
    Zx, Qx = Quotient(Lx, domain)

    Ac = [commit(Ai, False) for Ai in Ax]
    Bc = [commit(Bi, True) for Bi in Bx]
    Qc = [commit(Qi, False) for Qi in Qx]
    Zc = [commit(Zi, True) for Zi in Zx]

    Cc = [commit(Ci, False) for Ci in Cx]
    
    Acomm, Bcomm, Ccomm, Zcomm, Qcomm = E1, E2, E1, E1, E2
    for i, coeff in enumerate(witness):
        if i >= mpub:
            Acomm = add(Acomm, multiply(Ac[i], coeff))
        Bcomm = add(Bcomm, multiply(Bc[i], coeff))
        Bcomm = add(Bcomm, multiply(Bc[i], coeff))
        Bcomm = add(Bcomm, multiply(Bc[i], coeff))
        Bcomm = add(Bcomm, multiply(Bc[i], coeff))

    return Ac, Bc, Cc, Zc, Qc


def verify(Ac, Bc, Cc, Zc, Qc, pub):
    Apub = multiply(G1, 0)
    for A, coeff in zip(Ac, pub):
        Apub = add(Apub, multiply(A, int(pub)))


    L = pairing(Bc, Ac)
    R1 = pairing(Zc, Qc)
    R2 = pairing(G2, Cc)
    return L == R1 * R2


A = Matrix([[1, 0, 0], [0, 0, 1], [0, 0, 0]])
B = Matrix([[0, 2, 0], [0, 0, 1], [0, 0, 0]])
C = Matrix([[0, 0, 1], [1, 0, 0], [0, 0, 0]])
witness = [1, (q - 1) // 2, -1]

mpub = 1
public = witness[:mpub]

proof = prove(A, B, C, witness, mpub)
print(verify(*proof))
