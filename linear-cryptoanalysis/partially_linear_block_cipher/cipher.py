from data import sb, perm
from random import randint

rounds = 5
block = 4


def keygen():
    key = []
    for i in range(rounds):
        d = [randint(0, 255) for _ in range(block)]
        key.append(d)
    return key


def xor(a, b):
    return [x ^ y for x, y in zip(a, b)]


def sub(c):
    for i in range(len(c)):
        c[i] = sb[c[i]]


def bitify(arr):
    c = int.from_bytes(bytes(arr), "big")
    c = bin(c)[2:].zfill(8 * block)
    return c


def unbitify(arr):
    c = int(arr, 2)
    c = list(c.to_bytes(block, "big"))
    return c


def permute(c):
    ans = ["" for i in range(8 * block)]
    for i in range(len(c)):
        ans[perm[i]] = c[i]
    return ans


def encrypt(pt, key):
    ct = [x for x in pt]
    for j in range(3):
        ct = xor(ct, key[j])
        sub(ct)
        ct = unbitify("".join(permute(bitify(ct))))

    ct = xor(ct, key[3])
    sub(ct)
    ct = xor(ct, key[4])
    return ct


def cbc(pt, iv, key):
    pts = [pt[i : i + 4] for i in range(0, len(pt), 4)]
    cts = []

    ct = [x for x in pts[0]]
    ct = xor(ct, iv)
    ct = encrypt(ct, key)
    cts.append(ct)
    for i in range(1, len(pts)):
        ct = [x for x in pts[i]]
        ct = xor(ct, cts[-1])
        ct = encrypt(ct, key)
        ct.append(ct)
    ans = []
    for i in ct:
        ans += i
    return ans


def challenge():
    key = keygen()
    v = 0
    for i in range(0x3FFF):
        if int(input()) == 1:
            c = bytes.fromhex(input())
            c = encrypt(c, key)
            print(bytes(c).hex())
        else:
            if v < 16:
                iv = [randint(0, 255) for _ in range(4)]
                pt = [randint(0, 255) for _ in range(32)]
                ct = cbc(pt, iv, key)
                print(bytes(iv).hex())
                print(bytes(ct).hex())
                pt1 = bytes.fromhex(input())
                if pt == pt1:
                    print("PIZDAT")
                else:
                    print("Invalid Ct")
                v += 1


# challenge()
if __name__ == "__main__":
    n = 2**16 # 2**32 - number of connections
    bit31 = 0
    bit0 = 0
    bit7 = 0
    for i in range(n):
        key = keygen()
        pt = list(b"abob")
        ct = encrypt(pt, key)
        if (
            ct[-1] & 1
            == (pt[-1] + key[0][3] + key[1][3] + key[2][3] + key[3][3] + key[4][3]) & 1
        ):
            bit31 += 1

        if (
            ct[0] & 0b10000000
            == (pt[0] ^ key[0][0] ^ key[1][0] ^ key[2][0] ^ key[3][0] ^ key[4][0]) & 0b10000000
        ):
            bit0 += 1

        if ct[3] & 0b10 == (
            (pt[1] & 0b1)
            ^ (key[0][1] & 0b1)
            ^ (key[1][3] & 0b100)
            ^ (key[2][2] & 0b1)
            ^ (key[3][3] & 0b10)
            ^ (key[4][3] & 0b10)
        ):
            bit7 += 1

    print(bit31 / n)
    print(bit0 / n)
    print(bit7 / n)

    # key = keygen()
    # key = [0xa0, 0x4e, 0x7c, 0x8, 0x5c, 0xbb, 0xe4, 0xb6, 0xc4, 0x85, 0x94, 0xcd, 0xf0, 0xb7, 0xfd, 0xd0, 0x7c, 0x69, 0xa7, 0x52]
    # key = [key[i:i+4] for i in range(0, len(key), 4)]
    # p1 = b'aboa'
    # c1 = encrypt(p1, key)
    # print(b'aboa'.hex())
    # print(bytes(c1).hex())
    # p2 = b'rora'
    # c2 = encrypt(p2, key)
    # c4 = encrypt([x^y for x, y in zip(p1, p2)], key)

    # print(c1, c2, [x ^ y for x, y in zip(p1, p2)])
