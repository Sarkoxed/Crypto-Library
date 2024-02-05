import sys

r1cs_file = open(sys.argv[1], 'rb').read()

crs = 0
header = r1cs_file[crs:crs+4]
crs += 4
version = r1cs_file[crs:crs+4]
crs += 4
sections = r1cs_file[crs:crs+4]
crs += 4
contents = []
for i in range(int.from_bytes(sections, 'little')):
    s1t = r1cs_file[crs:crs+4]
    crs += 4
    s1s = r1cs_file[crs:crs+8]
    crs += 8
    content = r1cs_file[crs:crs+int.from_bytes(s1s, 'little')]
    crs += int.from_bytes(s1s, 'little')
    contents.append(content)
    print(s1t)

constraints = contents[0]
headers = contents[1]
wire2label = contents[2]

crs = 0
field_size  = int.from_bytes(headers[crs:crs+4], 'little')
crs += 4 
prime = int.from_bytes(headers[crs:crs+field_size],'little')
print(f"{prime=}")
crs += field_size
nwires = int.from_bytes(headers[crs:crs+4], 'little')
crs += 4
nPubOut = int.from_bytes(headers[crs:crs+4], 'little')
crs += 4
nPubIn = int.from_bytes(headers[crs:crs+4], 'little')
crs += 4
nPrvIn = int.from_bytes(headers[crs:crs+4], 'little')
crs += 4
nLabels = int.from_bytes(headers[crs:crs+8], 'little')
crs += 8
mConstr = int.from_bytes(headers[crs:crs+4], 'little')
crs += 4

print(f"{nwires, nPubOut, nPubIn, nPrvIn, nLabels, mConstr = }")

crs = 0
na = int.from_bytes(constraints[crs:crs+4], 'little')
print(f"{na=}")
crs += 4
for _ in range(na):
    wireId = int.from_bytes(constraints[crs:crs+4], 'little')
    print(f"{wireId = }")
    crs += 4
    a = int.from_bytes(constraints[crs:crs+field_size], 'little')
    crs += field_size
    print(a)

nb = int.from_bytes(constraints[crs:crs+4], 'little')
print(f"{nb=}")
crs += 4
for _ in range(na):
    wireId = int.from_bytes(constraints[crs:crs+4], 'little')
    print(f"{wireId = }")
    crs += 4
    b = int.from_bytes(constraints[crs:crs+field_size], 'little')
    crs += field_size
    print(b)
nc = int.from_bytes(constraints[crs:crs+4], 'little')
print(f"{nc=}")
crs += 4
for _ in range(na):
    wireId = int.from_bytes(constraints[crs:crs+4], 'little')
    print(f"{wireId = }")
    crs += 4
    c = int.from_bytes(constraints[crs:crs+field_size], 'little')
    crs += field_size
    print(c)

sage: prime=21888242871839275222246405745257275088548364400416034343698204186575808495617
sage: g = GF(prime)
sage: g(-7358504996770508486687187130827958137520805565857056985433965719766776637594).sqrt()
129520422605123408465286009268734000016285719319805644018060897281315512701
sage: int(g(-7358504996770508486687187130827958137520805565857056985433965719766776637594).sqrt()).to_bytes(16, 'little')
---------------------------------------------------------------------------
OverflowError                             Traceback (most recent call last)
Cell In[4], line 1
----> 1 int(g(-Integer(7358504996770508486687187130827958137520805565857056985433965719766776637594)).sqrt()).to_bytes(Integer(16), 'little')

OverflowError: int too big to convert
sage: int(g(-7358504996770508486687187130827958137520805565857056985433965719766776637594).sqrt()).to_bytes(32, 'little')
b'}!!!SC1R_ni_edih_ot_gnihtoN{SNI\x00'
sage: int(g(-7358504996770508486687187130827958137520805565857056985433965719766776637594).sqrt()).to_bytes(32, 'big')
b'\x00INS{Nothing_to_hide_in_R1CS!!!}'
