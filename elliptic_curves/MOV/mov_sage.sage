# Curve parameters
p = 17
a, b = 1, -1

# Target secret key
d = 8

# Setup curve
E = EllipticCurve(GF(p), [a, b])
G = E.gen(0)

P = d * G

# Find the embedding degree
# p**k - 1 === 0 (mod order)
order = E.order()
k = 1
while (p**k - 1) % order:
    k += 1

var('a')
K.<a> = GF(p**k)
EK = E.base_extend(K)
PK = EK(P)
GK = EK(G)
QK = EK.lift_x(a + 2)  # Independent from PK
AA = PK.tate_pairing(QK, E.order(), k)
print(AA)
GG = GK.tate_pairing(QK, E.order(), k)
print(GG)
dlA = AA.log(GG)

print(dlA)
