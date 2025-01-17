from Crypto.Util.number import getPrime, isPrime
from sage.all import GF, EllipticCurve, randint


def setup(nbit):
    p = 2**18 * 3**13 - 1
    E = EllipticCurve(GF(p**2, "i", modulus=[1, 0, 1]), [1, 0])
    assert E.is_supersingular()
    return E, 18, 13


E, ea, eb = setup(128)

P2, Q2 = E.torsion_basis(2**ea)
P3, Q3 = E.torsion_basis(3**eb)

s_A = randint(0, 2**ea)
K_A = P2 + s_A * Q2
K_A.set_order(2**ea)
phi_A = E.isogeny(kernel=K_A, algorithm="factor")

Alice_pub = (phi_A.codomain(), phi_A(P3), phi_A(Q3))
Alice_sec = s_A


s_B = randint(0, 3**eb)
K_B = P3 + s_B * Q3
K_B.set_order(3**eb)
phi_B = E.isogeny(kernel=K_B, algorithm="factor")

Bob_pub = (phi_B.codomain(), phi_B(P2), phi_B(Q2))
Bob_sec = s_B


K_BA = Bob_pub[1] + Alice_sec * Bob_pub[2]
K_BA.set_order(2**ea)
Shared_A = Bob_pub[0].isogeny(kernel=K_BA, algorithm="factor").codomain().j_invariant()

K_AB = Alice_pub[1] + Bob_sec * Alice_pub[2]
K_AB.set_order(3**eb)
Shared_B = (
    Alice_pub[0].isogeny(kernel=K_AB, algorithm="factor").codomain().j_invariant()
)

assert Shared_A == Shared_B
