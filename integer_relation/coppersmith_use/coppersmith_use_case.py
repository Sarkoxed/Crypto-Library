from sage.all import *
from out import n, e, hint, c

a = crt(hint, list(range(1, 199)))
b = lcm(list(range(1, 199)))
var('x')
F = Zmod(n)[x]
x0 = int(F(a + x * b).monic().small_roots(X=2**512 // b, beta=0.4)[0])

p = a + x0 * b
q = n // p
d = pow(e, -1, (p-1)*(q-1))
m = pow(c, d, n)
from Crypto.Util.number import long_to_bytes
print(long_to_bytes(m))
