from sage.all import var, PolynomialRing, GF

x, y, z = var("x, y, z")

orderings = ["lex", "deglex", "degrevlex"]
for order in orderings:
    P = PolynomialRing(GF(7), [x, y, z], order=order)
    f = P(x * y + 3 * y * z - 3)
    g = P(x**2 - 2 * y**2)


    I = P.ideal(x * y + z, y**3 + 1, z**2 - x *5 - 1)
    # print(I.variety())
    
    print(I.groebner_basis())
print(I)
