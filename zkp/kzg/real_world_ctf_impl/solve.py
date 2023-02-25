from pwn import remote
from sage.all import *

r = remote("47.254.47.63", 13337)
r.recvline()
r.recvline()
r.recvline()
msg = r.recvline().strip()
msg = msg.decode('utf-8')
msg = eval(msg)
PK, PKa = msg
print(len(PK))


p = 21888242871839275222246405745257275088696311157297823662689037894645226208583
e = EllipticCurve(GF(p), [0, 3])
PK = [e(x) for x in PK]
PKa = [e(x) for x in PKa]

print(len(PK), len(PKa))

c = [720, -1764, 1624, -735, 175, -21, 1]
print(len(c))
h = [30, -11, 1]

PiC = e((0, 1, 0))
PiCa = e((0, 1, 0))

PiH = e((0, 1, 0))

for i in range(len(c)):
    PiC += PK[i] * c[i]
    PiCa += PKa[i] * c[i]

for i in range(len(h)):
    PiH += PK[i] * h[i]
print(PiC, PiCa, PiH)


msg = f"({PiC.xy()[0]}, {PiC.xy()[1]}), ({PiCa.xy()[0]}, {PiCa.xy()[1]}), ({PiH.xy()[0]}, {PiH.xy()[1]})"
print(msg)
r.sendline(msg.encode())
r.interactive()
tmp = msg.replace('(','').replace(')','').replace(',','')
tmp = tmp.split(' ')
print(tmp)
PiC = (int(tmp[0].strip()),int(tmp[1].strip()))
PiCa = ((int(tmp[2].strip())),(int(tmp[3].strip())))
PiH = ((int(tmp[4].strip())),(int(tmp[5].strip())))

print(PiC, PiCa, PiH)
