from des_params import IP, FP, Shifts, PBox, EBox, SBox, pc1_table, pc2_table


class DES:
    def __init__(self, key: bytes):
        if len(key) != 8:
            raise ValueError(f"Invalid key length {len(key)}")
        self.key = key
        self.rounds = 16
        self.key_schedule()

    def bytestring_to_bitstring(self, bs):
        return [int(x >> i) & 1 for x in bs for i in reversed(range(8))]

    def bitstring_to_bytestring(self, bs):
        res_i = sum(bs[::-1][i] * 2**i for i in range(len(bs)))
        return res_i.to_bytes(8, "big")

    def permute(self, block, p):
        res_size = len(p)
        res = [0 for _ in range(res_size)]
        for j, i in enumerate(p):
            res[j] = block[i - 1]
        return res

    def key_schedule(self):
        round_keys = []

        current_key = self.bytestring_to_bitstring(self.key)
        current_key = self.permute(current_key, pc1_table)
        C0, D0 = current_key[:28], current_key[28:]

        for r in range(self.rounds):
            sh = Shifts[r]
            C0 = C0[sh:] + C0[:sh]
            D0 = D0[sh:] + D0[:sh]

            cur_key = C0 + D0
            cur_key_perm = self.permute(cur_key, pc2_table)
            round_keys.append(cur_key_perm)

        self.round_keys = round_keys

    def sbox(self, block, block_no):
        row = block[0] * 2 + block[-1]
        column = sum(2**i * block[1:5][::-1][i] for i in range(4))
        el_no = 16 * row + column
        return [int(x) for x in bin(SBox[block_no][el_no])[2:].zfill(4)]

    def F(self, hblock, key):
        exp = self.permute(hblock, EBox)
        xd = [a ^ b for a, b in zip(exp, key)]
        sd = []
        for i in range(0, len(xd), 6):
            sd += self.sbox(xd[i : i + 6], i // 6)
        return self.permute(sd, PBox)

    def _round(self, block, r):
        left = block[:32]
        right = block[32:]
        xs = self.F(right, self.round_keys[r])

        new_right = [a ^ b for a, b in zip(xs, left)]
        new_left = right
        return new_left + new_right

    def encrypt_block(self, block_):
        block = self.bytestring_to_bitstring(block_)
        block = self.permute(block, IP)

        for r in range(self.rounds):
            block = self._round(block, r)

        block = block[32:] + block[:32]
        block = self.permute(block, FP)
        return self.bitstring_to_bytestring(block)

    def decrypt_block(self, block_):
        block = self.bytestring_to_bitstring(block_)
        block = self.permute(block, IP)

        for r in reversed(range(self.rounds)):
            block = self._round(block, r)

        block = block[32:] + block[:32]
        block = self.permute(block, FP)
        return self.bitstring_to_bytestring(block)


class DES3:
    def __init__(self, key: bytes):
        if len(key) != 24:
            raise ValueError(f"Invalid key length {len(key)}")

        self.c1 = DES(key[:8])
        self.c2 = DES(key[8:16])
        self.c3 = DES(key[16:])

    def encrypt_block(self, block):
        t1 = self.c1.encrypt_block(block)
        t2 = self.c2.decrypt_block(t1)
        t3 = self.c3.encrypt_block(t2)
        return t3

    def decrypt_block(self, block):
        t1 = self.c3.decrypt_block(block)
        t2 = self.c2.encrypt_block(t1)
        t3 = self.c1.decrypt_block(t2)
        return t3


def test_des():
    from Crypto.Cipher import DES as des

    key = b"\xc9\xa4dY\xdd\x8c\xa9\xa0"
    data = b")\xd8\x15\xc86\xd5\xa9d"

    c = DES(key)
    enc = c.encrypt_block(data)

    assert enc == des.new(key=key, mode=des.MODE_ECB).encrypt(data)
    assert data == c.decrypt_block(enc)


def test_des3():
    from Crypto.Cipher import DES3 as des3

    key = b"\x1d*\x82P\xf3\x0f\xde\xc5\xe2\xa0\xd0\x93\xd7\xec*\x92\xbc/ -#\xb2rU"
    data = b")\xd8\x15\xc86\xd5\xa9d"

    c = DES3(key)
    enc = c.encrypt_block(data)

    assert enc == des3.new(key=key, mode=des3.MODE_ECB).encrypt(data)
    assert data == c.decrypt_block(enc)


if __name__ == "__main__":
    test_des()
    test_des3()
