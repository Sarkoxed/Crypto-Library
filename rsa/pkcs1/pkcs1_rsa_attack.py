from Crypto.Util.number import getPrime, long_to_bytes, bytes_to_long
from random import randint
from os import urandom
from gmpy2 import mpq


#class tp:
#    def __repr__(self):
#        return "(%d,%d)" % (self.start, self.end)
#
#    def __init__(self, start, end):
#        self.start = start
#        self.end = end
#
#    def __iter__(self):
#        yield self.start
#        yield self.end
#
#
#def union(s):
#    s.sort(key=lambda self: self.start)
#    y = [s[0]]
#    for x in s[1:]:
#        if y[-1].end < x.start:
#            y.append(x)
#        elif y[-1].end == x.start:
#            y[-1].end = x.end
#    return y


def pkcs1(m, n):
    k = len(long_to_bytes(n))

    if len(m) > k - 11:
        raise ValueError(f"lol n = {n}, k ={k}, m = {m}, len(m) = {m}")
    p = k - 3 - len(m)
    while True:
        pad = urandom(p)
        if b"\x00" not in pad:
            break
    return b"\x00\x02" + pad + b"\x00" + m

def unpkcs1(m, n):
    k = len(long_to_bytes(n))

    if len(m) != k - 1:
        raise ValueError("Wrong padding")
    ind = m.index(b'\x00')
    m = m[ind + 1:]
    return m

#m, c, n, e, p, q = 71746441411828173297087567717640288139365499633422852450, 820444514657395697484278084110707348003929433714415745803863, 935232064328678774065466014217583925592523306940360213146479, 65537, 1240669791121342883032663582309, 753812231926270077594115896131
p, q = getPrime(200), getPrime(200)
n = p * q
e = 65537
d = pow(e, -1, (p - 1) * (q - 1))


def valid_pkcs(c):
    k = len(long_to_bytes(n))
    r = pow(c, d, n)
    r = b"\x00" + long_to_bytes(r)
    if len(r) != k:
        return False
    if r[1] != 2:
        return False
    return True


def attack(c, e, n):
    print("Started attack")
    k = len(long_to_bytes(n))
    B = pow(2, 8 * (k - 2))
    B3 = 3 * B
    B2 = 2 * B

    if valid_pkcs(c):
        s0 = 1
    else:
        while True:
            s0 = randint(1, n - 1)
            c0 = (c * pow(s0, e, n)) % n
            if valid_pkcs(c0):
                break

    c0 = (c * pow(s0, e, n)) % n
    Ms = set([(B2, B3 - 1)])
#    print(Ms)
#    print("___" * 20)
    i = 1

    s = mpq(n, B3)

    while True:
 #       print("Round = ", i, end=" ", flush=True)
        if len(Ms) >= 2:
            for si in range(s + 1, n):
                c1 = (c0 * pow(si, e, n)) % n
                if valid_pkcs(c1):
                    s = si
                    break

        elif len(Ms) == 1:
            a, b = list(Ms)[0]
            flag = False

            ri_start = int(mpq(2 * (b * s - B2), n).__ceil__())
            for ri in range(ri_start, n):
                si_start = int(mpq(B2 + ri * n, b).__ceil__())
                si_end = int(mpq(B3 - 1 + ri * n, a).__floor__())

                for si in range(si_start, si_end + 1):
                    c1 = (c0 * pow(si, e, n)) % n
                    if valid_pkcs(c1):
                        s = si
                        flag = True
                        break
                if flag:
                    break

        tmp = set([])
        for a, b in Ms:
            r_lower = int(mpq(a * s - B3 + 1, n).__ceil__())
            r_upper = int(mpq(b * s - B2, n).__floor__())
            for r in range(r_lower, r_upper + 1):
                a1 = int(mpq(B2 + r * n, s).__ceil__())
                b1 = int(mpq(B3 - 1 + r * n,  s).__floor__())
                newa = max(a, a1)
                newb = min(b, b1)
                if newa <= newb:
                    tmp.add((newa, newb))

        if len(tmp) > 0:
            Ms = tmp

 #       print("Ms = ", len(Ms), end=" ", flush=True)
 #       flag = any(x <= m <= y for x, y in Ms)
 #       if flag:
 #           print("True ", end = " ", flush = True)
 #       else:
 #           print("False", end =" ", flush=True)

 #       print(Ms)

        if len(Ms) == 1:
            a, b = list(Ms)[0]
            if a == b:
                print(f"Finished in {i} rounds")
                return (a * pow(s0, -1, n)) % n
        i = i + 1


m = b"aboba"
m = pkcs1(m, n)
m = bytes_to_long(m)
#print(m)
c = pow(m, e, n)

a = attack(c, e, n)
if a == m:
    print("Successfully decrypted: ", unpkcs1(long_to_bytes(a), n))
else:
    print("Something went wrong...")
    print(f"m, c, n, e, p, q, a = {m}, {c}, {n}, {e}, {p}, {q}, {a}")
