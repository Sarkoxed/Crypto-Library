import cvc5
from cvc5 import Kind

s = cvc5.Solver()
s.setOption("produce-models", "true")
F = s.mkFiniteFieldSort("101")
a = s.mkConst(F, "a")
b = s.mkConst(F, "b")

inv = s.mkTerm(
        Kind.EQUAL,
        s.mkTerm(Kind.FINITE_FIELD_MULT, a, b),
        s.mkFiniteFieldElem("1", F)
        )
aIsTwo = s.mkTerm(
        Kind.EQUAL,
        a, 
        s.mkFiniteFieldElem("1", F)
        )

s.assertFormula(inv)
s.assertFormula(aIsTwo)
r = s.checkSat()
print(r)
