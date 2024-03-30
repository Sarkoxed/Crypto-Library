import cvc5
from cvc5 import Kind
from random import randint

n = 15

s = cvc5.Solver()
s.setOption("produce-models", "true")

bv = s.mkBitVectorSort(n)
x1 = s.mkConst(bv, "x")
x2 = s.mkConst(bv, "x1")

xor = s.mkTerm(Kind.BITVECTOR_XOR, x1, x2)
sub = s.mkTerm(Kind.BITVECTOR_SUB, x1, x2)

# x1_bits = [s.mkTerm(s.mkOp(Kind.BITVECTOR_EXTRACT, i, i), x1) for i in range(n)]
# x2_bits = [s.mkTerm(s.mkOp(Kind.BITVECTOR_EXTRACT, i, i), x2) for i in range(n)]

# for i in range(n):
#    s.assertFormula(s.mkTerm(Kind.EQUAL, x1_bits[i], s.mkBitVector(1, 1)))

delta1 = [s.mkConst(bv, f"x{i}") for i in range(n)]
for x in delta1:
    s.assertFormula(
        s.mkTerm(
            Kind.OR,
            s.mkTerm(Kind.EQUAL, x, s.mkBitVector(n, 1)),
            s.mkTerm(Kind.EQUAL, x, s.mkBitVector(n, 0)),
            s.mkTerm(Kind.EQUAL, x, s.mkBitVector(n, 2**n - 1)),
        )
    )
delta_sums1 = [
    s.mkTerm(Kind.BITVECTOR_MULT, s.mkBitVector(n, 2**i), xi)
    for i, xi in enumerate(delta1)
]
delta_sum1 = s.mkTerm(Kind.BITVECTOR_ADD, *delta_sums1)

delta2 = [s.mkConst(bv, f"x{i}") for i in range(n)]
for x in delta2:
    s.assertFormula(
        s.mkTerm(
            Kind.OR,
            s.mkTerm(Kind.EQUAL, x, s.mkBitVector(n, 1)),
            s.mkTerm(Kind.EQUAL, x, s.mkBitVector(n, 0)),
            s.mkTerm(Kind.EQUAL, x, s.mkBitVector(n, 2**n - 1)),
        )
    )
delta_sums2 = [
    s.mkTerm(Kind.BITVECTOR_MULT, s.mkBitVector(n, 2**i), xi)
    for i, xi in enumerate(delta2)
]
delta_sum2 = s.mkTerm(Kind.BITVECTOR_ADD, *delta_sums2)

s.assertFormula(s.mkTerm(Kind.EQUAL, sub, delta_sum1))
s.assertFormula(s.mkTerm(Kind.EQUAL, sub, delta_sum2))

for i in range(n):
    x12 = s.mkTerm(Kind.BITVECTOR_MULT, delta1[i], delta1[i])
    s.assertFormula(
        s.mkTerm(
            Kind.EQUAL,
            s.mkTerm(s.mkOp(Kind.BITVECTOR_EXTRACT, 0, 0), x12),
            s.mkTerm(s.mkOp(Kind.BITVECTOR_EXTRACT, i, i), xor),
        )
    )
    x12 = s.mkTerm(Kind.BITVECTOR_MULT, delta2[i], delta2[i])
    s.assertFormula(
        s.mkTerm(
            Kind.EQUAL,
            s.mkTerm(s.mkOp(Kind.BITVECTOR_EXTRACT, 0, 0), x12),
            s.mkTerm(s.mkOp(Kind.BITVECTOR_EXTRACT, i, i), xor),
        )
    )


nes = []
for i in range(n):
    nes.append(s.mkTerm(Kind.NOT, s.mkTerm(Kind.EQUAL, delta1[i], delta2[i])))
s.assertFormula(s.mkTerm(Kind.OR, *nes))

s.assertFormula(s.mkTerm(Kind.EQUAL, delta1[-1], delta2[-1]))

print(s.checkSat())

print(s.getValue(x1))
print(s.getValue(x2))
print(s.getValue(xor))
print(s.getValue(sub))
print()
print([s.getValue(xi).toPythonObj() for xi in delta1])
print([s.getValue(xi).toPythonObj() for xi in delta2])
