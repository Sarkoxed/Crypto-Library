def readbinfile(filename, type, maxversion):
    fd = open(filename, "rb")
    b = fd.read(4)
    readedType = b.decode()
    if readedType != type:
        return None
    v = int.from_bytes(fd.read(4), 'little')
    if v > maxversion:
        return None

    sections = dict()
    nsections = int.from_bytes(fd.read(4), 'little')
    for i in range(nsections):
        ht = int.from_bytes(fd.read(4), "little")
        hl = int.from_bytes(fd.read(8), "little")
        r = sections.setdefault(ht, [])
        r.append({"p": fd.tell(), "size": hl})
        sections[ht] = r
        fd.seek(hl, 1)
    return fd, sections

def readSection(fd, sections, idsection):
    if idsection not in sections:
        return None, 0
    if len(sections[idsection]) > 1:
        return None, 1
    fd.seek(sections[idsection][0]["p"], 0)
    readingsection = sections[idsection]
    return readingsection

def readHeader(fd, sections):
    reading = readSection(fd, sections, 1)
    n8 = int.from_bytes(fd.read(4), 'little')
    q = int.from_bytes(fd.read(n8), 'little')
    nWitness = int.from_bytes(fd.read(4), 'little')
    return n8, q, nWitness

def read(filename):
    fd, sections = readbinfile(filename, "wtns", 2)
    res = []
    n8, p, nWitness = readHeader(fd, sections)

    reading = readSection(fd, sections, 2)
    for i in range(nWitness):
        v = int.from_bytes(fd.read(n8), 'little')
        res.append(v)
    fd.close()
    return {"p": p, "wit": res}

def writesection(fd, data):
    datalen

def write(witness: dict, filename: str):
    prefix = b"wtns"
    version = b"\x02\x00\x00\x00"
    nsections = b"\x02\x00\x00\x00"
    
    n8 = (32).to_bytes(4, 'little')
    p = witness["p"].to_bytes(32, 'little')
    nwit = len(witness["wit"]).to_bytes(4, 'little')

    section1 = n8+p + nwit
    section1_prefix = b'\x01\x00\x00\x00' + len(section1).to_bytes(8, 'little')
    section1 = section1_prefix + section1

    section2 = b''
    for w in witness["wit"]:
        section2 += w.to_bytes(32, 'little')

    section2_prefix = b"\x02\x00\x00\x00" + len(section2).to_bytes(8, 'little')
    section2 = section2_prefix + section2
    
    sections = section1 + section2
    data = prefix + version + nsections + sections
    with open(filename, 'wb') as f:
        f.write(data)

if __name__ == "__main__":
    filename = "circom/witness/password.wtns"
    wit = read(filename)
    print(wit)
    write(wit, "tmp.wtns")
