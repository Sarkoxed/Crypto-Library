def shift(a):
    return a ^ (a >> 47)

def hasH_a(key):
    mul = (0xc6a4a793 << 32) + 0x5bd1e995
    
    lenn = len(key)
    buf = key

    len_aligned = (lenn >> 3) << 3

    hsh = (0xc70f6907 ^ (lenn * mul))  % 2**64
    print(f"alpha = {hsh}")

    for i in range(0, len_aligned, 8):
        tmp = int.from_bytes(buf[i:i + 8], 'little')
        data = shift(tmp * mul % 2**64) * mul % 2**64
        hsh ^= data
        hsh = (hsh  * mul) % 2**64

    lenn &= 7
    
    if lenn:
        tmp = key[-lenn:]
        data = int.from_bytes(tmp, 'little')
        print(data)
        hsh ^= data
        hsh = (hsh * mul) % 2**64

    
    alpha = ((lenn * mul) % 2**64) ^ 0xc70f6907
    d0 = int.from_bytes(key[:8])
    d1 = int.from_bytes(key[8:])
#    assert hsh == (((((alpha ^ (shift(d0 * mul % 2**64) * mul % 2**64)) * mul) % 2**64) ^ d1) * mul) % 2**64
    print(f"beta = {hsh}")
    hsh = shift(hsh) * mul
    hsh = shift(hsh % 2**64)

    return hsh

def unshift(a):
    tmp = a >> 47
    return a ^ tmp

from random import randint
def unhash(hsh, lenn, taillen):
    mul = (0xc6a4a793 << 32) + 0x5bd1e995

    hsh = unshift(hsh)
    hsh = (hsh * pow(mul, -1, 2**64)) % 2**64
    hsh = unshift(hsh)

    beta = hsh
#    print(f"{beta = }")

    alpha = ((lenn * mul) % 2**64) ^ 0xc70f6907
#    print(f"{alpha = }")

    d1 = randint(0, 2**(taillen * 8) - 1)
#    print(d1)
    pre_d0 = (((beta * pow(mul, -1, 2**64) % 2**64 ) ^ d1) * pow(mul, -1, 2**64) % 2**64) ^ alpha

    d0 = pre_d0 * pow(mul, -1, 2**64) % 2**64
    d0 = unshift(d0)
    d0 = d0 * pow(mul, -1, 2**64) % 2**64
#    print(d0)

    assert (((((alpha ^ (shift(d0 * mul % 2**64) * mul % 2**64)) * mul) % 2**64) ^ d1) * mul) % 2**64 == beta

    return d0.to_bytes(8, 'little') + d1.to_bytes(lenn & 7, 'little')


#ret = hasH_a(b"govno")
#print(hasH_a(b'g' * 17))

#c = randint(0, 2**64 - 1)
#
#res = unhash(c, 10, 2)
#print(f"{c = }")
#print(f"{res = }")
#print(hasH_a(res))
#print(len(res))
#print()

res = unhash(10987361646061798740, 15, 7)
print(res)
print(hasH_a(res))


print("\\x".join(hex(x)[2:].zfill(2) for x in res))
