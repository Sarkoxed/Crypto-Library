from sage.all import EllipticCurve, GF, randint, PolynomialRing


class Public:
    def __init__(
        self,
        p=21888242871839275222246405745257275088696311157297823662689037894645226208583,
        a=0,
        b=3,
        q=21888242871839275222246405745257275088548364400416034343698204186575808495617,
        G1=(1, 2),
        d=100,
    ):
        self.e = EllipticCurve(GF(p), [a, b])
        self.g = self.e(G1)
        self.q = q
        tau = randint(0, q)  # trusted setup lol

        self.powers = [self.g]
        for _ in range(d):
            self.powers.append(tau * self.powers[-1])


# lagrange form of basis
# TODO Batch proof, multi-point proof generation(FK algorithm 2020)


class Prover:
    def __init__(self, p: Public):
        self.p = p
        self.ring = PolynomialRing(GF(self.p.p), var('x'))
        self.poly = self.ring.random_element(degree=100)

    def commit(self, poly=self.poly):
        com = self.p.e((0, 1, 0))
        for coeff, power in zip(poly.coefficients, self.p.powers):
            com += coeff * power
        return com

    def zerotest_arbitrary_set(self, teta, poly, r):
        arg = self.poly.args()[0]
        vanishing_poly = product(self.ring(x - a) for a in teta)
        assert poly % vanishing_poly == 0
        quotient = poly // vanishing_poly
        return self.commit(poly), self.commit(quotient), (poly(x=r), qutient(x=r))
    
    def zerotest_subgroup(self, q, omega, poly, r):
        arg = self.poly.args()[0]
        vanishing_poly = self.ring(x^q - 1)
        assert poly % vanishing_poly == 0
        quotient = poly // vanishing_poly
        return self.commit(poly), self.commit(quotient), (poly(x=r), qutient(x=r))

    # def sum_check()

    def product_check(self, q, omega, poly, r): # TODO rational functions
        ts = [poly(x=1)]
        for j in range(1, omega.multiplicative_order()):
            ts.append(ts[-1] * poly(x=pow(omega, j)))

        # t = interpolate(ts, omega, q) TODO
        
        x = poly.args()[0]
        poly = t(omega*x) - t * poly(omega * x)        # assert that t(w * r) - t(r) * f(w * r) = q(r) * (r^k - 1)
        t_com, q_com, ev_r = self.zerotest_subgroup(q, omega, t, r)
        tt_com, qq_com, evv_r = self.zerotest_arbitrary_set([pow(omega, q-1)], t - 1, r) # bruh
        return t_com, q_com, ev_r, tt_com, qq_com, evv_r
    
    # given (f(1), f(omega), ..., f(omega^{q-1})), (g(1), g(omega), ..., g(omega^{q-1})) - permutation of f
    def permutation_check(self, teta, f, g, r):
        # Prod (r - f(a)) / (r - g(a)) = 1

    def prescribed_permutation_check(self, f, g, W, teta):
        # (W(a), f(a)) - perm of (a, g(a)) than f(y) = g(W(y)) for every y in teta)

        # f(X, Y) = product (X - Y * W(a) - f(a))
        # g(X, Y) = product (X - Y * a - g(a))
        # productCheck product((r - s * W(a) - f(a)) / (r - ss * a - g(a))) = 1
