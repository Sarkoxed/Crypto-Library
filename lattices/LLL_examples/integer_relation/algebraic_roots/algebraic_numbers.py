from sage.all import *


def get_poly(n, d, a):
    m = identity_matrix(n+1)
    m = m.T.insert_row(n+1, vector([floor(10**d * a**(n-i)) for i in range(n+1)])).T
#    print(m)
    v = m.LLL()[0]
    var('x')
#    print(v)
    return sum(x**(len(v) - i - 2)  * v[i] for i in range(len(v)-1))

if __name__ == "__main__":
    a, d, p = float(input("alpha: ")), int(input("prop degree: ")), int(input("prec: "))
    print(get_poly(d, p, a))
