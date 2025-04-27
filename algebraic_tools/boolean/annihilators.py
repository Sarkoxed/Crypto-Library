from sage.all import BooleanPolynomialRing, Matrix, GF, prod, var
from sage.crypto.boolean_function import BooleanFunction
from sage.sat.boolean_polynomials import solve as solve_sat

# https://www.researchgate.net/publication/4298760_Several_Algorithms_to_find_Annihilators_of_Boolean_Function
# TODO do it in coefficent forms. Same since h(xn) = 0 <=> ci = 0

from itertools import combinations
def get_Ad(xs, d):
    n = len(xs)
    basis = []
    for k in range(0, min(d, n)+1):
        tmp = [prod(monom) for monom in combinations(xs, r=k)]
        basis += tmp
    return basis

def get_Cd(f, xs, d):
    basis = get_Ad(xs, d)
    res = set()
    for p in basis:
        res.add(f * p)
    return res

def get_Md(f, xs, d):
    basis = get_Ad(xs, d)
    M = []
    for p in basis:
        M.append([int(x) for x in BooleanFunction(p * f).truth_table()])
    return Matrix(GF(2), M)

def get_annihilators(f, xs, d):
    n = len(xs)
    Md = get_Md(f, xs, d)
    Ker = Md.kernel()
    Ad = get_Ad(xs, d)
    anns = []
    for v in Ker.basis():
        anns.append(sum(Ad[i] for i, j in enumerate(v) if j == 1))
    return anns

if __name__ == "__main__":
    s = [[0, 1, 2, 3], [0, 1, 2, 4, 5], [0, 1, 2, 5], [0, 1, 2], [0, 1, 3, 4, 5], [0, 1, 3, 5], [0, 1, 3], [0, 1, 4], [0, 1, 5], [0, 2, 3, 4, 5], [0, 2, 3], [0, 3, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4], [1, 2, 3, 5], [1, 2], [1, 3, 5], [1, 3], [1, 4], [1], [2, 4, 5], [2, 4], [2], [3, 4], [4, 5], [4], [5]]
    xs = [var(f'x{i}') for i in range(6)]
    B = BooleanPolynomialRing(6, xs)
    xsb = [B(x) for x in xs]
    poly1 = sum(prod([xsb[i] for i in p]) for p in s)
    
    
    ann0 = get_annihilators(poly1, xsb, 3)
    ann1 = get_annihilators(poly1+1, xsb, 3)
    print(ann0)
    print(ann1)

    assert all(poly1 * ann == 0 for ann in ann0)
    assert all((poly1  + 1) * ann == 0 for ann in ann1)
