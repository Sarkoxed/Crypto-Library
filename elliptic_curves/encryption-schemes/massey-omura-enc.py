from sage.all import EllipticCurve, GF, random_prime, randint, gcd, ZZ

p = random_prime(2**128)
E = EllipticCurve(GF(p), [1, 2])
N = E.order()
G = GF(p)

M_t = int.from_bytes(b"Hey Bubs", "big") << 50
while True:
    r = randint(0, 2**50)
    M1 = M_t + r
    if G(M1**3 + M1 + 2).is_square():
        break

M = E.lift_x(ZZ(M1))
mA = randint(0, M.order())
while gcd(mA, N) != 1:
    mA //= gcd(mA, N)
M1 = mA * M

mB = randint(0, N)
while gcd(mB, N) != 1:
    mB //= gcd(mB, N)
M2 = mB * M1

M3 = M2 * (pow(mA, -1, N))
M4 = M3 * (pow(mB, -1, N))

print((int(M4[0]) >> 50).to_bytes(8, "big"))
