from string import ascii_lowercase, ascii_uppercase, digits
alph = ascii_uppercase + ascii_lowercase + digits + "+/"
print(len(alph))
assert len(alph) == 64

def base64encode(m: bytes):
    padlen = 0 
    padding = ""
    if len(m) * 8 % 6 != 0:
        padding = "=" * (len(m)  % 3)
        padlen = (6 - len(m) * 8 % 6)
    b = "".join(bin(x)[2:].zfill(8) for x in m) + '0' * padlen
    print(b)
    blocks = [int(b[i:i+6], 2) for i in range(0, len(b), 6)]
    enc = "".join(alph[i] for i in blocks) + padding
    return enc.encode()

def test(n = 1000):
    from os import urandom
    from random import randint
    from base64 import b64encode

    for _ in range(n):
        t = urandom(randint(1, 100))
        try:
            assert base64encode(t) == b64encode(t)
        except:
            print(t)
            print(base64encode(t))
            print(b64encode(t))
            exit()
 

if __name__ == "__main__":
    test()
