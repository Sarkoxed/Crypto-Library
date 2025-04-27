#!/usr/local/bin/python
from hashlib import sha256

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import random
from ast import literal_eval

if __name__ != "__main__":
    raise Exception("not a lib?")

from os import urandom

seed = int.from_bytes(urandom(8), "little")

random.seed(seed)
print(random.getstate()[1][:10])

idxs = literal_eval(input(">>> "))
if len(idxs) > 8:
    print("Ha thats funny")
    exit()
for idx in range(624):
    rand_out = random.getrandbits(32)
    if idx in idxs:
        print(rand_out)


key = random.getrandbits(256)
nonce = random.getrandbits(256)
flag = open("flag.txt").read()
aes_key = sha256(str(key).encode()).digest()[:16]
aes_nonce = sha256(str(nonce).encode()).digest()[:16]
cipher = AES.new(aes_key, AES.MODE_GCM, nonce=aes_nonce)
ct = cipher.encrypt(pad(flag.encode(), 16))
print(ct.hex())
