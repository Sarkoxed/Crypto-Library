from pwn import remote
import json
from Crypto.Util.number import long_to_bytes, bytes_to_long
from random import randint, choices
import re
from attack import attack

host, port = "socket.cryptohack.org", 13396

r = remote(host, port)

resp = r.recvline().decode()

name = re.findall(r"Player (.*).", resp)[0][:16]
print(name)
name = bytes.fromhex(name)
cur = name[-1]

a = 0x1337deadbeef
b = 0xb
m = 2**48

payload = {"option": "get_a_challenge"}
payload = json.dumps(payload).encode()
r.sendline(payload)

resp = r.recvline().decode()
resp = json.loads(resp)

pt = bytes.fromhex(resp["plaintext"])
iv = bytes.fromhex(resp["IV"])

key0 = []
s0 = attack(pt[-8:], 48, 8, 2**48, a, b)[-1]
for i in range(8):
    s0 = (a * s0 + b) % 2**48
    key0.append(s0)
key0 = [x >> 40 for x in key0]

key1 = []
s0 = attack(iv[:8], 48, 8, 2**48, a, b)[0]
for i in range(8):
    s0 = ((s0 - b) * pow(a, -1, 2**48)) % 2**48
    key1.append(s0)
key1 = [x >> 40 for x in key1]
key = key0 + key1[::-1]
key = bytes(key)

from Crypto.Cipher import AES
cipher = AES.new(key, AES.MODE_CBC, iv)

ct = cipher.encrypt(pt).hex()

payload = {"option": "validate", "ciphertext": ct}
print(payload)
r.sendline(json.dumps(payload).encode())
print(r.recvline())
