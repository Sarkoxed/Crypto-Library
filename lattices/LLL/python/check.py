from LLL_improved import *
from LLL import LLL_own
from copy import copy


def LLL_check(base, delta=3/4, eta=1/2):
    w = [vector(x) for x in Matrix(base).gram_schmidt()[0]]
    mu = [[base[i].dot_product(w[j]) / w[j].norm()**2 for j in range(len(base))] for i in range(len(base))]
#    print(mu)
    for i in range(len(mu)):
        for j in range(len(mu)):
            assert i == j or abs(mu[i][j]) <= eta
    for i in range(1, len(base)):
        assert w[i].norm()**2 >= (delta - mu[i][i-1]**2) * w[i-1].norm()**2


def hadam(x):
    return pow(abs(det(x))/prod(vector(y).norm() for y in x), 1/len(list(x)))


s = list()
for i in range(10):
    print(i)
    a = randint(2, 20)
    M = MatrixSpace(ZZ, a, a) 
    m = M.random_element()
    while(m.det() == 0):
        m = M.random_element()
    m1 = Matrix(copy(m))
    m2 = [vector(x) for x in copy(m)]

    try:
        c1 = m1.LLL(delta=3/4, eta=1/2)
        c2 = Matrix(LLL_imporved(m2, 0.75))
        assert (abs(c1.det()) == abs(c2.det()) and abs(c1.det()) == abs(m.det())) and (hadam(c1) == hadam(c2))
        LLL_check([vector(x) for x in c2])
        LLL_check([vector(x) for x in c1])
    except AssertionError:
        print(list(m))
        print()
        print("Sage\n",list(c1), hadam(c1), c1.det())
        print()
        print("Improved\n",list(c2), hadam(c2), c2.det())
        print()
        c3 = LLL_own([vector(x) for x in m])
        print("Old\n", list(c3), hadam(Matrix(c3)), Matrix(c3).det())
    except Exception as e:
        print(list(m))
        print(e)
        break
