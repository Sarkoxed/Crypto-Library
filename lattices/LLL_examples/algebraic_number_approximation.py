# algdep(x, n)

from sage.all import Matrix, PolynomialRing, var, ZZ, RR, ceil, log, QQ, floor, identity_matrix, randint, gcd

# |ci| < 10^b, |alpha - beta| < 10^-a, a >= b * n + epsilon * n^2

n = 20
x = var('x')
p = PolynomialRing(ZZ, x).random_element(degree=n-1)
while len(p.change_ring(RR).roots()) == 0:
    p = PolynomialRing(ZZ, x).random_element(degree=n-1) 

beta = p.change_ring(RR).roots()[0][0]
b = max(ceil(abs(log(c))/log(10)) for c in p.coefficients())
print(b)

a = randint(b * n, b * n + 10)
alpha = RR(floor(beta * 10**a)) / RR(10**a)

m = Matrix(QQ, n, n+1)
m.set_block(0, 0, identity_matrix(n))
m.set_block(0, n, Matrix([floor(10**a * alpha**i) for i in range(n)]).T)

print(p.change_ring(RR).roots()[0])
print()
for c in m.LLL():
    p1 = PolynomialRing(ZZ, x)(list(c)[:-1])
    print(p1.change_ring(RR).roots())
