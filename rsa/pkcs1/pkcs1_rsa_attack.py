from Crypto.Util.number import getPrime, long_to_bytes, bytes_to_long
from random import randint
from os import urandom
from gmpy2 import mpq


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

#p, q = getPrime(500), getPrime(500)
#n = p * q
#e = 65537
#d = pow(e, -1, (p - 1) * (q - 1))
#m = b"aboba"
#m = pkcs1(m, n)
#m = bytes_to_long(m)
##print(m)
#c = pow(m, e, n)


m, c, n, e, p, q, a = 0x206218e8c5e3b527a162ea56184e18012b6b982098bfe86d408d144f7296442186248f37016bc3eb256dfb1ff0a262f991b79cd7749299515f75a1115bff2bf0994d1f0b0d603c2a105a18e9a9910043ded1ed1eb1f242184d31322e001157cd7b3a9fa55519ee21d5973c94cde0d67bf574ebb14e50061626f6261, 0x51af6f1638a957e2946e8a98afff5d1710ab43594b63fc01397720f88e89f54342b9f5eec8eb92b8fb4e381b5cda391b92ea242bea4baa7eb50a53d37bd385b5825a407fe95c5f787bb468f8d7fc0ec1b5d181e14bb790afd4d754ffc2c867c729b714351eb5db86961f7d416a297f02eb38f0ab838991f2e5c1f9f584, 0x8da842199cf73a7ece7e236131c2b522846ec2b1c913a18f122ac30ed2324715447f140152ac3519399e53cd9b671ff2d9c4539ff3f9b4f05dd78e2b592ab86043546735f52a96db45874b3d377fe9ea2b4e05486eed2c47fd79047467b4245827fb1c98551d2de31a1a40826b8035ecb1f3b67cc82eb5783595b9c447, 0x10001, 0xe82ac35e9afe3210e3ba8a863ba9aa91504c97dcc4f53ea32d2228acbba95784ce004757ae7632da6d44f3dc1bb7fb4310c87c8fc8cbb9eedf602646b1265, 0x9c32f124fdb987c8073cca6ee6d572b21ad03be79fbc9aaa1676e751573f38f5a5feb8fcf31af5cfb2efbea2d740d0ab8a68b859eb56cc55c8efe53fe7b3b, 0x206218e8c5e3b527a162ea56184e18012b6b982098bfe86d408d144f7296442186248f37016bc3eb256dfb1ff0a262f991b79cd7749299515f75a1115bff2bf0994d1f0b0d603c2a105a18e9a9910043ded1ed1eb1f242184d31322e001157cd7b3a9fa55519ee21d5973c94cde0d67bf574ebb14e50061626f6261
d = pow(e, -1, (p-1)*(q-1))

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

    oracle_calls = 0

    if valid_pkcs(c):
        oracle_calls += 1
        s0 = 1
    else:
        while True:
            s0 = randint(1, n - 1)
            c0 = (c * pow(s0, e, n)) % n
            oracle_calls += 1
            if valid_pkcs(c0):
                break

    c0 = (c * pow(s0, e, n)) % n
    Ms = set([(B2, B3 - 1)])
    i = 1

    s = mpq(n, B3)

    while True:
 #       print("Round = ", i, end=" ", flush=True)
        if len(Ms) >= 2:
            for si in range(s + 1, n):
                c1 = (c0 * pow(si, e, n)) % n
                oracle_calls += 1
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
                    oracle_calls += 1
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
            print(r_upper - r_lower)
            exit(0)
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
                print(f"Finished in {i} rounds. Oracle calls: {oracle_calls}. Modulus bit length: {k * 8}")
                return (a * pow(s0, -1, n)) % n
        i = i + 1


from time import time

t_start = time()
a = attack(c, e, n)
t_end = time()
print("Time passed: ", t_end - t_start)
if a == m:
    print("Successfully decrypted: ", unpkcs1(long_to_bytes(a), n))
else:
    print("Something went wrong...")
    print(f"m, c, n, e, p, q, a = {m}, {c}, {n}, {e}, {p}, {q}, {a}")
print(f"m, c, n, e, p, q, a = {m}, {c}, {n}, {e}, {p}, {q}, {a}")

