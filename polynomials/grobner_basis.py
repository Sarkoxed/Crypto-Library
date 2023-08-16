from sage.all import GF, var

def reduce(p, d): # not the same as p % d since it will produce x1 * x2 % x1 * x2 + x3 = x1 * x2 not -x3
    mon = d.lm()
    t = None
    for _, _t in list(p):
        if mon.divides(_t):
            t = _t
            break
    
    if t is not None:
        return p - t / mon * d  # only one term? bruh

def reduce_set(p, D):
    for d in D:
        tmp = reduce(p, d)  # only once?
        if tmp is not None:
            return tmp

def spoly(p, q):
    return p * q.lm() - q * p.lm()

def is_grobner(G):
    

def grobner_basis(G):
    while not all()
x1, x2 = var('x1 x2')
f = GF(101)[x1, x2]
a1 = f.random_element()
a2 = f.random_element()
print(a1)
print(a2)
print(reduce(a1, a2))
print(reduce(a2, a1))
