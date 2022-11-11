from Crypto.Util.strxor import strxor

n = 512
h0 = b'\x00' * n
def sha1(d: bytes):
    d = b'\x00' * (len(d) % n) + d
    d = [d[i:i+n] for i in range(0, len(d), n)]
    h = h0
    for dx in range(d):
        h = strxor(h, add_hoc(dx))
    return h

def add_hoc(d: bytes):

