rotl64 = lambda x, n: ((x << n) | x >> (64 - n)) & (2**64 - 1)

def fmix64(k):
    k ^= k >> 33
    k = (k * 0xff51afd7ed558ccd) & (2**64 - 1)
    k ^= k >> 33
    k = (k * 0xc4ceb9fe1a85ec53) & (2**64 - 1)
    k ^= k >> 33
    return k

def MurmurHash3_x64_128 (key, seed=0):
    nblocks = len(key) // 16
    
    h1 = seed
    h2 = seed
    
    c1 = 0x87c37b91114253d5;
    c2 = 0x4cf5ad432745937f;
      
    
    blocks = [int.from_bytes(key[i: i + 8], 'little') for i in range(0, len(key), 8)]
    for i in range(nblocks):
        k1 = blocks[2 * i]
        k2 = blocks[2 * i + 1]

        k1 = (k1 * c1) & (2**64 - 1)
        k1 = rotl64(k1, 31)
        k1 = (k1 * c2) & (2**64 - 1)
        h1 ^= k1
        h1 = rotl64(h1, 27)
        h1 += h2
        h1 = (h1*5+0x52dce729) & (2**64 - 1)

        k2 = (k2 * c2) & (2**64 - 1)
        k2 = rotl64(k2, 33)
        k2 = (k2 * c1) & (2**64 - 1)
        h2 ^= k2
        h2 = rotl64(h2, 31)
        h2 += h1
        h2 = (h2*5+0x38495ab5) & (2**64 - 1)

    tail = key[nblocks * 16:]
    
    k1 = 0
    k2 = 0
    
    if len(tail) > 0:
        k1 = int.from_bytes(tail[:8], 'little')
        k1 = (k1 * c1) & (2**64 - 1)
        k1 = rotl64(k1, 31)
        k1 = (k1 * c2) & (2**64 - 1)
        h1 ^= k1

        k2 = int.from_bytes(tail[8:], 'little')
        k2 = (k2 * c2) & (2**64 - 1)
        k2 = rotl64(k2, 33)
        k2 = (k2 * c1) & (2**64 - 1)
        h2 ^= k2


    h1 ^= len(key)
    h2 ^= len(key)

    h1 += h2
    h2 += h1
    h1 %= 2**64
    h2 %= 2**64


    h1 = fmix64(h1)
    h2 = fmix64(h2)

    h1 += h2
    h2 += h1
    h1 %= 2**64
    h2 %= 2**64

    return hex(h1)[2:].zfill(16) + hex(h2)[2:].zfill(16)

if __name__ == "__main__":
    m = b'\xf6\x07v\x1e\x80i\x87\xe2*\xdc\xea<+\xd9\x92\xfbluiwjXvIOUMRNHK'

    print(MurmurHash3_x64_128(m))
