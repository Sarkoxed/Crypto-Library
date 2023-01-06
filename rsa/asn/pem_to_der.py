import sys
from base64 import b64decode

f = open(sys.argv[1], "rt").read().split('\n')[1:-1]
f = ''.join(f)

if sys.argv[2] == '1':
    r = b64decode(f.encode())
    with open(sys.argv[1].replace("pem", "der"), "wb") as w:
        w.write(r)
else:
    r = b64decode(f.encode() + b'=======')
    with open(sys.argv[1].replace("pem", "der"), "wb") as w:
        w.write(r)
