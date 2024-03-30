from sage.all import *
from out import n, e, hint, c

a = crt(hint, list(range(1, 199)))
b = lcm(list(range(1, 199)))
var('x')
F = Zmod(n)[x]
x0 = F(a + x * b).monic().small_roots(X=2**512 // b, beta=0.4)
print(x0)
x0 = int(x0[0])
print(F(a + x * b)(x=x0))

p = int(a) + int(x0) * int(b)
print(p)
assert p < n

q = n // p
d = pow(e, -1, (p-1)*(q-1))
m = pow(c, d, n)
from Crypto.Util.number import long_to_bytes
print(long_to_bytes(m))
