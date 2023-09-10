# crypto.standford.edu/pbc/notes/ep/tonelli.html


from sage.all import *

def tonelli_sqrt(a, p):
    while True:
        g = randint(0, p)
        if pow(g, (p - 1)//2, p) != 1:
            break

    s, t = 0, p - 1
    while t % 2 == 0:
        t //= 2
        s += 1

    e = 0
    for i in range(2, s + 1):
        if pow(a * pow(g, -e, p), (q-1) // pow(2, i)) != 1:
            e = pow(2, i-1) + e
    h = a * pow(g, -e, p) % p
    b = pow(g, e//2, p) * pow(h, (t+1)//2, p)
    return b

p = random_prime(10000000)
a = randint(0, p)
while pow(a, (p-1)//2, p) == 1:
    a = randint(0, p)

b = tonelli_sqrt(a, p)
print(b)
print(pow(b, 2, p))
print(a)
