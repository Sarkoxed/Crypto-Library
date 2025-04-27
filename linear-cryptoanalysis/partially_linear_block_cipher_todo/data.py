perm = {i: (i // 8) + 4 * (i % 8) for i in range(32)}

sb = """20h, 1, 52h, 93h, 4, 0A5h, 0C6h, 5Fh, 38h, 9, 8Ah, 3Bh
0Ch, 5Dh, 8Eh, 37h, 8, 21h, 2Ah, 0CBh, 64h, 4Dh, 0E6h
67h, 88h, 29h, 0A2h, 83h, 2Ch, 65h, 2Eh, 7, 0B0h, 19h
72h, 3, 1Ch, 25h, 1Eh, 4Fh, 0, 71h, 62h, 0ABh, 14h
7Dh, 76h, 6Fh, 28h, 0A9h, 1Ah, 5Bh, 0C4h, 45h, 96h
0Fh, 30h, 91h, 12h, 63h, 9Ch, 75h, 0A6h, 47h, 10h, 61h
5Ah, 13h, 8Ch, 1Dh, 4Eh, 3Fh, 0A0h, 0B9h, 4Ah, 33h
94h, 2Dh, 7Eh, 97h, 58h, 0E1h, 0AAh, 0Bh, 54h, 35h
16h, 57h, 0E0h, 99h, 0DAh, 2Bh, 34h, 0C5h, 5Eh, 2Fh
0A8h, 0A1h, 22h, 0E3h, 4Ch, 8Dh, 0AEh, 17h, 80h, 31h
9Ah, 43h, 3Ch, 0CDh, 46h, 1Fh, 78h, 0F9h, 42h, 9Bh
0ECh, 0B5h, 3Eh, 8Fh, 98h, 39h, 2, 0DBh, 24h, 9Dh, 36h
0DFh, 70h, 0F1h, 92h, 0B3h, 44h, 15h, 6, 27h, 48h, 0D1h
7Ah, 0BBh, 0FCh, 5, 0D6h, 0C7h, 90h, 81h, 82h, 6Bh
0B4h, 0EDh, 0F6h, 77h, 18h, 69h, 6Ah, 53h, 0DCh, 0Dh
9Eh, 0EFh, 68h, 49h, 0FAh, 73h, 0A4h, 55h, 6Eh, 87h
0D0h, 59h, 32h, 8Bh, 6Ch, 0ADh, 0Eh, 0D7h, 0B8h, 51h
0EAh, 23h, 5Ch, 95h, 0EEh, 7Fh, 40h, 11h, 0B2h, 0F3h
0E4h, 0FDh, 56h, 9Fh, 0F0h, 0E9h, 0E2h, 0EBh, 74h, 0F5h
66h, 0B7h, 0E8h, 0B1h, 0C2h, 0FBh, 7Ch, 3Dh, 0BEh, 0BFh
0D8h, 89h, 3Ah, 7Bh, 84h, 0E5h, 86h, 0F7h, 0C0h, 41h
0D2h, 0A3h, 0ACh, 0BDh, 26h, 0E7h, 0C8h, 0C1h, 0Ah
0C3h, 0F4h, 85h, 0DEh, 0A7h, 60h, 0C9h, 0BAh, 0D3h
0CCh, 0D5h, 0B6h, 0CFh, 50h, 0D9h, 0CAh, 1Bh, 0BCh
6Dh, 0CEh, 0FFh, 0F8h, 79h, 0F2h, 4Bh, 0D4h, 0DDh, 0FEh
0AFh"""

sb = sb.replace('\n', ', ').replace('h', '').split(", ")
sb = [int(x, 16) for x in sb]
if __name__ == "__main__":
    from sage.crypto.sbox import SBox
    from sage.all import Integer
    s = SBox(sb)
    al = s.linear_approximation_table()
    
    d = dict()
    for i in range(256):
        for j in range(256):
            x = al[i][j] / Integer(256) + Integer(1)/Integer(2)
            d.setdefault(x, [])
            d[x].append((i, j))
#        print(m.n(), bin(i)[2:].zfill(8), bin(r)[2:].zfill(8))
    r = list(d.items())
    r = sorted(r, key=lambda x: x[0], reverse=True)
    
    for prob, values in r:
        if prob <= 0.6:
            break
        for x in values:
            print(prob.n(), bin(x[0])[2:].zfill(8), bin(x[1])[2:].zfill(8), (bin(x[0])[2:].zfill(8)+ bin(x[1])[2:].zfill(8)).count('1') < 5)
        #c = min(values, key=lambda x: (bin(x[0]) + bin(x[1])).count('1'))
        #print(prob.n(), bin(c[0])[2:].zfill(8), bin(c[1])[2:].zfill(8))
    print("____________________")
    #for x in r:
    #    for y in x[1]:
    #        if (bin(y[0]) + bin(y[1])).count('1') < 5 and x[0] >= Integer(1) / Integer(2):
    #            print(x[0], bin(y[0])[2:].zfill(8), bin(y[0])[2:].zfill(8))
