import cvc5
from cvc5 import Kind
from random import randint

n = 15
x1 = randint(0, 2**n - 1)
x2 = randint(0, 2**n - 1)
d_xor = [int(x) for x in bin(x1 ^ x2)[2:].zfill(n)]
d = [int(x) for x in bin((x1 - x2) % 2**n)[2:].zfill(n)]

# d_xor = [1, 0, 0, 1, 1, 1, 1, 1, 1, 1]
# d = [1, 0, 0, 0, 0, 0, 1, 0, 1, 1]

s = cvc5.Solver()
s.setOption("produce-models", "true")

bv = s.mkBitVectorSort(n)
x1 = s.mkConst(bv, "x")
x2 = s.mkConst(bv, "x1")

s.assertFormula(
    s.mkTerm(
        Kind.EQUAL,
        s.mkTerm(Kind.BITVECTOR_XOR, x1, x2),
        s.mkBitVector(n, sum(2**i * xi for i, xi in enumerate(d_xor[::-1]))),
    )
)
s.assertFormula(
    s.mkTerm(
        Kind.EQUAL,
        s.mkTerm(Kind.BITVECTOR_SUB, x1, x2),
        s.mkBitVector(n, sum(2**i * xi for i, xi in enumerate(d[::-1]))),
    )
)

i = 0

sigs = set()
while s.checkSat().isSat():
    print(i)
    t1 = s.getValue(x1).toPythonObj()
    t2 = s.getValue(x2).toPythonObj()

    d_sig = [
        int(x1) - int(x2) for x1, x2 in zip(bin(t1)[2:].zfill(n), bin(t2)[2:].zfill(n))
    ]
    d_xor = [
        int(x1) ^ int(x2) for x1, x2 in zip(bin(t1)[2:].zfill(n), bin(t2)[2:].zfill(n))
    ]
    d_mod = [int(x) for x in bin((t1 - t2) % 2**n)[2:].zfill(n)]
    sigs.add(tuple(d_sig))

    i += 1

    s.assertFormula(
        s.mkTerm(
            Kind.OR,
            s.mkTerm(Kind.NOT, s.mkTerm(Kind.EQUAL, x1, s.getValue(x1))),
            s.mkTerm(Kind.NOT, s.mkTerm(Kind.EQUAL, x2, s.getValue(x2))),
        )
    )
    if i % 1000 == 0:
        for si in sigs:
            print(si)
        print()

for si in sigs:
    print(si)
print()
