from os import urandom
from Crypto.Cipher import DES

key = urandom(8)
cip = DES.new(key=key, mode=DES.MODE_ECB)

key_inv = bytes(x ^ 0xFF for x in key)
cip_inv = DES.new(key=key_inv, mode=DES.MODE_ECB)

m = urandom(8)

c = cip.encrypt(m)

c_inv = bytes(x ^ 0xFF for x in c)
m_inv = cip_inv.decrypt(c_inv)

m1 = bytes(x ^ 0xFF for x in m_inv)
assert m == m1
