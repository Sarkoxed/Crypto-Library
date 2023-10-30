def reverse_fmix(k):
    k ^= k >> 33
    k = (k * pow(0xc4ceb9fe1a85ec53, -1, 2**64)) % 2**64
    k ^= k >> 33
    k = (k * pow(0xff51afd7ed558ccd, -1, 2**64)) % 2**64
    k ^= k >> 33
    return k

rotl64 = lambda x, n: ((x << n) | x >> (64 - n)) & (2**64 - 1)
rotr64 = lambda x, n: rotl64(x, 64 - n)

def reverse_murmurhash_le15(hashstr: str, length):
    h = int(hashstr, 16)

    h2 = h % 2**64 
    h1 = h >> 64    
    
    h2 -= h1
    h1 -= h2

    h1 %= 2**64
    h2 %= 2**64

    h2 = reverse_fmix(h2)
    h1 = reverse_fmix(h1)

    h2 -= h1
    h1 -= h2
    h1 %= 2**64
    h2 %= 2**64
   
    h1 ^= length
    h2 ^= length

    len15 = length & 15

    c1 = 0x87c37b91114253d5
    c2 = 0x4cf5ad432745937f

    if 1 <= length < 16:
        k1 = h1
        k1 = (k1 * pow(c2, -1, 2**64)) % 2**64
        k1 = rotr64(k1, 31)
        k1 = (k1 * pow(c1, -1, 2**64)) % 2**64

        k2 = h2
        k2 = (k2 * pow(c1, -1, 2**64)) % 2**64
        k2 = rotr64(k2, 33)
        k2 = (k2 * pow(c2, -1, 2**64)) % 2**64
    else:
        print("unreversible")

    nblocks = length // 16

    return k1.to_bytes(8, 'little') + k2.to_bytes(8, 'little')


def get_zero_16_ntail_symbols(tail):
    c1 = 0x87c37b91114253d5
    c2 = 0x4cf5ad432745937f
    
    k1 = int.from_bytes(tail[:8], 'little')
    k2 = int.from_bytes(tail[8:], 'little')

    
    h1 = len(tail) + 16
    h2 = len(tail) + 16

    # BLOCK OF TALE
    k1 = (k1 * c1) & (2**64 - 1)
    k1 = rotl64(k1, 31)
    k1 = (k1 * c2) & (2**64 - 1)
    h1 = k1 ^ (len(tail) + 16)

    k2 = (k2 * c2) & (2**64 - 1)
    k2 = rotl64(k2, 33)
    k2 = (k2 * c1) & (2**64 - 1)
    h2 = k2 ^ (len(tail) + 16)


    # BLOCK before TAIL
    h2 = (h2 - 0x38495ab5) % 2**64
    h2 = (h2 * pow(5, -1, 2**64)) % 2**64
    h2 = (h2 - h1) % 2**64
    h2 = rotr64(h2, 31)
    k2 = h2

    k2 = (k2 * pow(c1, -1, 2**64)) % 2**64
    k2 = rotr64(k2, 33)
    k2 = (k2 * pow(c2, -1, 2**64)) % 2**64

    h1 = (h1 - 0x52dce729) % 2**64
    h1 = (h1 * pow(5, -1, 2**64)) % 2**64
    h1 = rotr64(h1, 27)
    k1 = h1

    k1 = (k1 * pow(c2, -1, 2**64)) % 2**64
    k1 = rotr64(k1, 31)
    k1 = (k1 * pow(c1, -1, 2**64)) % 2**64

    b1 = k1.to_bytes(8, 'little')
    b2 = k2.to_bytes(8, 'little')
    return b1 + b2

def get_zero_16():
    c1 = 0x87c37b91114253d5
    c2 = 0x4cf5ad432745937f
    
    h1 = 16
    h2 = 16

    # BLOCK before TAIL
    h2 = (h2 - 0x38495ab5) % 2**64
    h2 = (h2 * pow(5, -1, 2**64)) % 2**64
    h2 = (h2 - h1) % 2**64
    h2 = rotr64(h2, 31)
    k2 = h2

    k2 = (k2 * pow(c1, -1, 2**64)) % 2**64
    k2 = rotr64(k2, 33)
    k2 = (k2 * pow(c2, -1, 2**64)) % 2**64

    h1 = (h1 - 0x52dce729) % 2**64
    h1 = (h1 * pow(5, -1, 2**64)) % 2**64
    h1 = rotr64(h1, 27)
    k1 = h1

    k1 = (k1 * pow(c2, -1, 2**64)) % 2**64
    k1 = rotr64(k1, 31)
    k1 = (k1 * pow(c1, -1, 2**64)) % 2**64

    b1 = k1.to_bytes(8, 'little')
    b2 = k2.to_bytes(8, 'little')
    return b1 + b2

# works for seed 0
if __name__ == "__main__":
    from murmurhash3_128 import MurmurHash3_x64_128

    zero16 = get_zero_16()
    print(f"Murmur3_128({zero16}) = {MurmurHash3_x64_128(zero16)}")
    print()

    from string import ascii_lowercase, ascii_uppercase, digits
    alph = ascii_lowercase + ascii_uppercase + digits
    from random import choices, randint

    tail = "".join(choices(alph, k=15)).encode()
    hashtail15 = MurmurHash3_x64_128(tail)
    tail_rev = reverse_murmurhash_le15(hashtail15, 15)
    print(f"{tail, tail_rev = }")
    print()


    tail = "".join(choices(alph, k = 12)).encode()
    res = get_zero_16_ntail_symbols(tail)
    m = res + tail
    
    print(f"Known tail: {tail}")
    print(f"MurmurHash3_128({m}) =  {MurmurHash3_x64_128(m)}")
    print()
