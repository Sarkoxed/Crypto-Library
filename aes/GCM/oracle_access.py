from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor


class GHASH:
    tail = b""
    mod = (1 << 128) | (1 << 7) | (1 << 2) | (1 << 1) | 1
    x = 0
    adata_len = 0
    ct_len = 0
    final = None

    def __init__(self):
        return

    def get_counter(self, H: bytes, iv: bytes):
        self.H = self.bytes_to_gf(H)

        if len(iv) == 96 // 8:
            counter = iv + b"\x00\x00\x00\x01"
        else:
            curlen = len(iv) * 8
            padlen = (16 - (len(iv) % 16)) % 16
            iv += b"\x00" * padlen
            iv += b"\x00" * 8
            iv += curlen.to_bytes(8, "big")
            counter = self.__hash(iv)

        return counter

    def set_encrypted_counter(self, ectr: bytes):
        self.final = ectr

    @staticmethod
    def reverse(n):
        return int("{:08b}".format(n).zfill(128)[::-1], 2)

    @staticmethod
    def bytes_to_gf(b):
        return GHASH.reverse(int.from_bytes(b, "big"))

    @staticmethod
    def gf_to_bytes(b):
        return GHASH.reverse(b).to_bytes(16, "big")

    @staticmethod
    def mult(a, b):
        p = 0
        while a > 0:
            if a & 1:
                p = p ^ b
            a >>= 1
            b <<= 1
            if b & (1 << 128):
                b ^= GHASH.mod
        return p

    def __hash(self, data):
        x = 0
        padlen = (16 - (len(data) % 16)) % 16
        data += b"\x00" * padlen

        for i in range(0, len(data), 16):
            block = self.bytes_to_gf(data[i : i + 16])
            Xi = block ^ x
            Xi = self.mult(Xi, self.H)
            x = Xi

        return self.gf_to_bytes(Xi)

    def update(self, data, kind: bool = False):
        if kind:
            self.adata_len += len(data) * 8
        else:
            self.ct_len += len(data) * 8

        padlen = (16 - (len(data) % 16)) % 16
        data += b"\x00" * padlen

        for i in range(0, len(data), 16):
            block = self.bytes_to_gf(data[i : i + 16])
            Xi = block ^ self.x
            Xi = self.mult(Xi, self.H)
            self.x = Xi

    def get_tag(self):
        self.tail = self.adata_len.to_bytes(8, "big") + self.ct_len.to_bytes(8, "big")
        block = self.reverse(int.from_bytes(self.tail, "big"))
        Xi = block ^ self.x
        Xi = self.mult(Xi, self.H)
        self.x = Xi

        tag = self.gf_to_bytes(Xi)
        hashedtag = tag
        tag = strxor(tag, self.final)
        return tag


def test():
    from os import urandom
    from random import randint

    for _ in range(100):
        key = urandom(16)
        iv = urandom(randint(1, 16))
        pt = urandom(randint(1, 100))
        additional = urandom(randint(1, 100))

        cipher = AES.new(key, mode=AES.MODE_GCM, nonce=iv)
        cipher.update(additional)
        ct, tag = cipher.encrypt_and_digest(pt)

        gh = GHASH()

        cipher1 = AES.new(key, mode=AES.MODE_ECB)
        H = cipher1.encrypt(b"\x00" * 16)
        counter = gh.get_counter(H, iv)

        final = cipher1.encrypt(counter)
        gh.set_encrypted_counter(final)

        gh.update(additional, True)
        gh.update(ct, False)
        tag_own = gh.get_tag()
        assert tag_own == tag


if __name__ == "__main__":
    test()
