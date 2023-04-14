from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor

def reverse(n):
    return int('{:08b}'.format(n).zfill(128)[::-1], 2)



class GHASH:
    tail = b""
    mod = (1 << 128) | (1 << 7) | (1 << 2) | (1 << 1) | 1
    x = 0

    def __init__(self, key, iv):
        cipher = AES.new(key, mode=AES.MODE_ECB)
        H = cipher.encrypt(b"\x00" * 16)
        self.H = self.bytes_to_gf(H)
        # it seems that the higher bits -> lower in GF

        self.tail = b"\x00" * 8

        if len(iv) == 96 // 8:
            iv += b"\x00\x00\x00\x01"
            self.final = cipher.encrypt(iv)
        else:
            curlen = len(iv) * 8
            padlen = (16 - (len(iv) % 16)) % 16
            iv += b"\x00" * padlen
            iv += b"\x00" * 8
            iv += long_to_bytes(curlen, 8)
            self.final = cipher.encrypt(self.hash(iv))

            self.x = 0
            self.tail = b"\x00" * 8

    def bytes_to_gf(self, b):
        return reverse(bytes_to_long(b))

    def gf_to_bytes(self, b):
        return long_to_bytes(reverse(b), 16)

    def mult(self, a, b):
        p = 0
        while a > 0:
            if a & 1:
                p = p ^ b
            a >>= 1
            b <<= 1
            if b & (1 << 128):
                b ^= self.mod
        return p

    def update(self, adata):
        self.tail = long_to_bytes(len(adata) * 8, 8)
        padlen = (16 - (len(adata) % 16)) % 16
        adata = adata + b"\x00" * padlen

        for i in range(0, len(adata), 16):
            block = self.bytes_to_gf(adata[i: i + 16])
            Xi = block ^ self.x
            Xi = self.mult(Xi, self.H)
            self.x = Xi

    def hash(self, data):
        self.tail += long_to_bytes(len(data) * 8, 8)
        padlen = (16 - (len(data) % 16)) % 16
        data = data + b"\x00" * padlen

        for i in range(0, len(data), 16):
            block = self.bytes_to_gf(data[i: i + 16])
            Xi = block ^ self.x
            Xi = self.mult(Xi, self.H)
            self.x = Xi

        return self.gf_to_bytes(Xi)

    def get_tag(self):
        block = reverse(bytes_to_long(self.tail))
        Xi = block ^ self.x
        Xi = self.mult(Xi, self.H)
        self.x = Xi

        tag = self.gf_to_bytes(Xi)
        hashedtag = tag
        tag = strxor(tag, self.final)
        return tag

if __name__ == "__main__":
    from os import urandom
    from random import randint

    for i in range(10000):
        key = urandom(16)
        iv = urandom(randint(1, 16))
        pt = urandom(randint(1, 100))
        additional = urandom(randint(1, 100))
       

        cipher = AES.new(key, mode=AES.MODE_GCM, nonce=iv)
        cipher.update(additional)
        ct, tag = cipher.encrypt_and_digest(pt)

        gh = GHASH(key, iv)
        gh.update(additional)
        gh.hash(ct)
        tag_own = gh.get_tag()
        assert tag_own == tag
