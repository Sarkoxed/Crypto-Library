from sage.all import GF, PolynomialRing

p = 21888242871839275222246405745257275088548364400416034343698204186575808495617
F = GF(p)
x = var('x')
P = PolynomialRing(F, x)

beta = F.random_element()
delta = F.random_element()
