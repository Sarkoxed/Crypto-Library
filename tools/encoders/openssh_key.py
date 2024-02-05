from base64 import b64decode, b64encode
import sys

s1 = open(sys.argv[1], "rt").readlines()[1:-1]
s1 = "".join(x.strip() for x in s1)
print(s1[:100])
print(b64decode(s1[:100]))
s1 = s1.replace("?", "A")
s1 += "===="
res = b64decode(s1)

cur = 0
header = res[cur:cur+15]
cur += 15

ctnl = int.from_bytes(res[cur:cur+4], "big")
cur += 4
ciphername = res[cur:cur + ctnl]
print(f"{ciphername=}")
cur += ctnl

kdfl = int.from_bytes(res[cur:cur+4], "big")
cur += 4
kdfname = res[cur:cur + kdfl]
print(f"{kdfname}")
cur += kdfl

kdflen = int.from_bytes(res[cur:cur+4], "big")
cur += 4
print(f"{kdflen=}")


nkeys = int.from_bytes(res[cur:cur+4], "big")
cur += 4
print(f"{nkeys=}")

sshpubl = int.from_bytes(res[cur:cur+4], "big")
cur += 4
print(f"{sshpubl=}")

sshpub = res[cur:cur+sshpubl]
#res = res[:cur] + b'\x00\x00\x00\x13ecdsa-sha2-nistp256\x00\x00\x00\x08nistp256\x00\x00\x00A\x04{\xd8\x1a\xa9=\xd3{T\xe1\xd3\x9c\x04\xf4\xdbg\xdce\xe6\xb9R\x11\x07\xdd\x11\xc8\x0e\x87\x1e\xf3\xbdaK\x1a\x17\xadZQ\xb6\xccu\x17a\x88\x81p*#\xfe\x8c\xc6\xe4\xbb\x06\xaf:\\\\M\xc7\xb8L\xcf\x11\x08' + res[cur + sshpubl:]
#tmpres = b64encode(res).decode()
#b64res = '\n'.join(tmpres[i:i+70] for i in range(0, len(tmpres), 70))
#print(b64res)

cur += sshpubl
print(f"{sshpub=}")

rpcpl = int.from_bytes(res[cur:cur+4], "big")
cur += 4
print(f"{rpcpl=}")

dummychecksum = res[cur:cur+8]
print(f"{dummychecksum=}")
cur += 8

keytypel = int.from_bytes(res[cur:cur+4], "big")
cur += 4
print(f"{keytypel=}")

keytype = res[cur:cur+keytypel]
print(f"{keytype=}")
cur+=keytypel

pub0l = int.from_bytes(res[cur:cur+4], "big")
cur += 4
print(f"{pub0l=}")

pub0 = res[cur:cur+pub0l]
print(f"{pub0=}")
cur+=pub0l

pub1l = int.from_bytes(res[cur:cur+4], "big")
cur += 4
print(f"{pub1l=}")

pub1 = res[cur:cur+pub1l]
print(f"{pub1=}")
cur+=pub1l

print(res[cur:])

print(res[cur:])
prv0l = int.from_bytes(res[cur:cur+4], "big")
cur += 4
print(f"{prv0l=}")

prv0 = res[cur:cur+prv0l]
print(f"{prv0=}")
cur+=prv0l

if sys.argv[1] == "tmpecdsa2":
    prv0l = 32
    prv0 = res[cur:cur+prv0l]
    print(prv0)
    cur += prv0l

print(b64encode(prv0))
print(res[cur:])
