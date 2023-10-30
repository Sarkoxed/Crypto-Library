from sage.all import Matrix, GF
from Crypto.Util.number import getPrime

p = getPrime(1024)
while p % 4 == 3:
    p = getPrime(1024)

alpha = int(GF(p)(-1).sqrt())

M = Matrix([[p, 0], [alpha, 1]]).LLL()

a, b = M[0]

print(a, b)
print(a**2 + b**2 == p)
