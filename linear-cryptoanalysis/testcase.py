from sage.all import *
from sage.crypto.sbox import SBox

s = SBox((0xe, 4, 0xd, 1, 2, 0xf, 0xb, 8, 3, 0xa, 6, 0xc, 5, 9, 0, 7))
p = {1: 1, 2: 5, 3: 9, 4: 13, 5: 2, 6: 6, 7: 10, 8: 14, 9: 3, 10: 7, 11: 11, 12: 15, 13: 4, 14: 8, 15: 12, 16: 16}
la = s.linear_approximation_table()

key = [
        [0b0011, 0b1010, 0b1001, 0b0100],
        [0b1010, 0b1001, 0b0100, 0b1101],
        [0b1001, 0b0100, 0b1101, 0b0110],
        [0b0100, 0b1101, 0b0110, 0b0011],
        [0b1101, 0b0110, 0b0011, 0b1111]
    ]

# bias of x1 ^ x4 ^ y2, it equals 0 if #((0,0,0), (1, 1, 0), (1, 0, 1), (0, 1, 1)) check the sbox and determine that there's 8 cases sat. P[x1 + x4 + y2 = 0] = 8/16 = 1/2 => bias is 0
print(f"bias(x1 + x4 + y2) = {la[0b1001][0b100] / 16}")
# x3 + x4 + y1 + y4: again check the sbox and you'll have 
print(f"bias(x3 + x4 + y1 + y4) = {la[0b0011][0b1001]/ 16}")
