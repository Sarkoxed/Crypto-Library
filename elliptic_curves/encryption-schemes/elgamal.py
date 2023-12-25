from sage.all import EllipticCurve, random_prime, GF, randint, ZZ

p = random_prime(2**128)
E = EllipticCurve(GF(p), [1, 2])
N = E.order()
G = GF(p)

P = E.random_point()
s = randint(1, N - 1)
B = s * P


k = randint(1, N - 1)
M1 = k * P

M_t = int.from_bytes(b"Hey Bubs", "big") << 50
while True:
    r = randint(0, 2**50)
    M_ = M_t + r
    if G(M_**3 + M_ + 2).is_square():
        break
M = E.lift_x(ZZ(M_))

M2 = M + k * B


M3 = M2 - s * M1
print((int(M3[0]) >> 50).to_bytes(8, "big"))
