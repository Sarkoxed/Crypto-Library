from Crypto.Util.number import bytes_to_long, long_to_bytes

def gf_2_128_mul(x, y):
    assert x < (1 << 128)
    assert y < (1 << 128)
    res = 0
    for i in range(127, -1, -1):
        res ^= x * ((y >> i) & 1)  # branchless
        x = (x >> 1) ^ ((x & 1) * 0xE1000000000000000000000000000000)
    assert res < 1 << 128
    return res

class GHASH:
    def __init__(self, zkey):
        self.__auth_key = bytes_to_long(zkey)

        # precompute the table for multiplication in finite field
        table = []  # for 8-bit
        for i in range(16):
            row = []
            for j in range(256):
                row.append(gf_2_128_mul(self.__auth_key, j << (8 * i)))
            table.append(tuple(row))
        self.__pre_table = tuple(table)

        self.prev_init_value = None  # reset

    def __times_auth_key(self, val):
        res = 0
        for i in range(16):
            res ^= self.__pre_table[i][val & 0xFF]
            val >>= 8
        return res

    def ghash(self, txt):
        len_txt = len(txt)
        # padding
        if 0 == len_txt % 16:
            data = txt
        else:
            data += txt + b'\x00' * (16 - len_txt % 16)

        hash = 0
        for i in range(len(data) // 16):
            hash ^= bytes_to_long(data[i * 16: (i + 1) * 16])
            hash = self.__times_auth_key(hash)
        return long_to_bytes(hash)

    def tag(self, txt):
        len_txt = len(txt)
        tag = bytes_to_long(self.ghash(txt))
        tag ^= 8 * len_txt
        tag = self.__times_auth_key(tag)
        return long_to_bytes(tag)

gh = GHASH(b'\xf0' * 16)
print(gh.tag(b'\xa0' * 16))
