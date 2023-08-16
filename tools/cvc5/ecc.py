import cvc5 
from cvc5 import Kind


def double(x, y, s, F, i):
    lam = s.mkConst(F, f"lam{i}")
    tmp1 = s.mkTerm(Kind.FINITE_FIELD_MULT, s.mkFiniteFieldElem("2", F), y)
    tmp2 = s.mkTerm(Kind.FINITE_FIELD_MULT, tmp1, lam)
    tmp3 = s.mkTerm(Kind.FINITE_FIELD_MULT, x, x)
    tmp4 = s.mkTerm(Kind.FINITE_FIELD_MULT, s.mkFiniteFieldElem("3", F), tmp3)
    s.assertFormula(s.mkTerm(Kind.EQUAL, tmp2, tmp4))
    lam_sq = s.mkTerm(Kind.FINITE_FIELD_MULT, lam, lam)
    tmp5 = s.mkTerm(Kind.FINITE_FIELD_MULT, s.mkFiniteFieldElem("-2", F), x)
    x2 = s.mkTerm(Kind.FINITE_FIELD_ADD, tmp5, lam_sq)

    tmp6 = s.mkTerm(Kind.FINITE_FIELD_NEG, x2)
    tmp7 = s.mkTerm(Kind.FINITE_FIELD_ADD, x, tmp6)
    tmp8 = s.mkTerm(Kind.FINITE_FIELD_MULT, lam, tmp7)
    tmp9 = s.mkTerm(Kind.FINITE_FIELD_NEG, y)
    y2 = s.mkTerm(Kind.FINITE_FIELD_ADD, tmp8, tmp9)
    return x2, y2

def add(x1, y1, x2, y2, s, F, i):
    neg_y1 = s.mkTerm(Kind.FINITE_FIELD_NEG, y1)
    tmp1 = s.mkTerm(Kind.FINITE_FIELD_ADD, y2, neg_y1)

    neg_x1 = s.mkTerm(Kind.FINITE_FIELD_NEG, x1)
    tmp2 = s.mkTerm(Kind.FINITE_FIELD_ADD, x2, neg_x1)

    lam = s.mkConst(F, f"lam{i}")
    tmp3 = s.mkTerm(Kind.FINITE_FIELD_MULT, tmp2, lam)
    s.assertFormula(s.mkTerm(Kind.EQUAL, tmp3, tmp1))
    
    lam_sq = s.mkTerm(Kind.FINITE_FIELD_MULT, lam, lam)
    tmp4 = s.mkTerm(Kind.FINITE_FIELD_ADD, lam_sq, neg_x1)
    neg_x2 = s.mkTerm(Kind.FINITE_FIELD_NEG, x2)
    x3 = s.mkTerm(Kind.FINITE_FIELD_ADD, tmp4, neg_x2)

    neg_x3 = s.mkTerm(Kind.FINITE_FIELD_NEG, x3)
    tmp7 = s.mkTerm(Kind.FINITE_FIELD_ADD, x1, neg_x3)
    tmp8 = s.mkTerm(Kind.FINITE_FIELD_MULT, lam, tmp7)

    y3 = s.mkTerm(Kind.FINITE_FIELD_ADD, tmp8, neg_y1)
    return x3, y3

def mult(x, y, n, s, F):
    res = bin(n)[2:][1:]
    xr, yr= x, y
    j = 0
    for i in res:
        xr, yr  = double(xr, yr, s, F, j)
        j += 1
        if i == '1':
            xr, yr = add(xr, yr, x, y, s, F, j)
            j += 1
    return xr, yr


k = int(input("k: "))

s = cvc5.Solver()
s.setOption("produce-models", "true")
F = s.mkFiniteFieldSort("21888242871839275222246405745257275088696311157297823662689037894645226208583") 
x = s.mkConst(F, "x")
y = s.mkConst(F, "y")

xn, yn = mult(x, y, k, s, F)

s.assertFormula(s.mkTerm(Kind.EQUAL, s.mkTerm(Kind.EQUAL, x, s.mkFiniteFieldElem(0, F)), s.mkBoolean(0)))
#s.assertFormula(s.mkTerm(Kind.EQUAL, x, s.mkFiniteFieldElem("10683722752867610459204101586384809151674422591785948834172063774520050601540", F)))
#s.assertFormula(s.mkTerm(Kind.EQUAL, y, s.mkFiniteFieldElem("546908910574108510642716938153429601359088277061187212893383933333876997251", F)))

s.assertFormula(s.mkTerm(Kind.EQUAL, xn, x))
s.assertFormula(s.mkTerm(Kind.EQUAL, yn, y))

res = s.checkSat()
print(res.isSat())

if res.isSat():
    print("x", s.getValue(x).toPythonObj())
    print("y", s.getValue(y).toPythonObj())
