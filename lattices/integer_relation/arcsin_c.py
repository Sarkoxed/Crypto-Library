from sage.all import Matrix, RealField, sin, arcsin, log, ceil, floor, randint, algdep, pi

n = 1000
R = RealField(prec=n)
d = ceil(log(2**n) / log(10))



key = randint(2**255, 2**256)
print(f"{key = }")
alpha = R(sin(key))
print(f"{alpha=}")
P = algdep(alpha, 100)

# e = P(m) - recover P

rs = P.change_ring(R).roots()
pp = R(2 * pi) 
for r, _ in rs:
    if abs(r) > 1:
        continue
    tmp = arcsin(r)
    c3 = ceil(10**d * tmp)
    c2 = ceil(10**d * pp)
    c1 = 10**d

    M = Matrix([[1, 0, c1], 
                [0, 1, c2], 
                [0, 0, c3]]).LLL()
    print(abs(M[0][0]) == key)
    print(abs(M[0][0])//2 == key)
