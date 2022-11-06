from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.strxor import strxor

key = b"\x0a" * 16
iv = b"\x0b" * 16


def padding_oracle_cbc(c):
    v = [c[i : i + 16] for i in range(0, len(c), 16)]
    ans = b""
    for i in range(1, len(v)):
        cur = v[i]
        starti = b"\x00" * 16
        curacc = b""
        for j in range(1, 17):
            for k in range(256):
                start = starti[:-j] + bytes([k]) + curacc
                #print(start)
                p = start + cur
                try:
                    p = AES.new(key=key, iv=iv, mode=AES.MODE_CBC).decrypt(p)
                    p1 = unpad(p, 16)
                    curacc = bytes([k]) + curacc
#                    print(p, curacc)
                    break
                except ValueError:
                    continue
                except Exception as e:
                    print(e)
            if j < 16:
                curacc = strxor(curacc, bytes([j]) * len(curacc))
                curacc = strxor(curacc, bytes([j + 1]) * len(curacc))
#        print(curacc)
        deccur = strxor(curacc, b"\x10" * 16)
        deccur = strxor(deccur, v[i - 1])
        ans += deccur
        print(ans)


c = AES.new(key=key, iv=iv, mode=AES.MODE_CBC).encrypt(b"abobanaf" * 2 + b'roraloli' * 2+ b'kekrlole' * 2)
padding_oracle_cbc(c)
