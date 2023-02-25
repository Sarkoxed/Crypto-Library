from sage.all import PolynomialRing, GF, randint, product, var


def interpolate(values: list[int], p: int, l: int):
    vars = [var(f"x_{i}") for i in range(l)]

    poly = 0
    for i in range(2**l):
        point = [int(x) for x in bin(i)[2:].zfill(l)]
        delta = product(
            (point[i] * vars[i] + (1 - point[i]) * (1 - vars[i])) for i in range(l)
        )
        poly += values[i] * delta
    return poly


class Prover:
    def __init__(self, l: int, p: int, honest: bool):
        self.l = l
        self.p = p
        self.h = honest
        # self.values = [randint(0, p) for i in range(l)]
        # self.poly = interpolate(self.values, self.p, self.l)
        self.vars = [var(f"x_{i}") for i in range(l)]
        self.poly = PolynomialRing(GF(p), self.vars).random_element(terms=2**l) # not multilinear
        self.round_polys = [self.poly]
        self.round = 0

    @staticmethod
    def rec_sum(deep, end, rnd, poly):
        if deep == end:
            return poly
        ans = Prover.rec_sum(deep + 1, end, rnd, poly)
        arg = poly.args()[deep]
        if rnd <= deep:
            return eval(f"ans({arg}=0) + ans({arg}=1)")
        return ans

    def get_sum(self):
        ans = Prover.rec_sum(0, self.l, 0, self.poly)
        return ans

    def get_round_poly(self, r: int):
        ans = 0
        crp = self.round_polys[self.round]
        self.round_polys.append(eval(f"crp({self.vars[self.round]}={r})"))
        self.round += 1

        ans = Prover.rec_sum(0, self.l, self.round, crp)
        return ans

    def get_evaluation(self, points: list[int]):
        assert len(points) == self.l

        ans = self.poly
        for y in range(self.l):
            ans = eval(f"ans({self.vars[y]}={points[y]})")
        return ans


def verify(P: Prover):
    l, p = P.l, P.p

    points = [randint(0, p - 1) for _ in range(l)]

    print("Asking for sum")
    s = P.get_sum()
    cur = s

    for i in range(l):
        print(f"round {i}")
        si = P.get_round_poly(points[i])
        arg = si.args()[i]
        assert eval(f"si({arg}=0) + si({arg}=1)") == cur
        cur = eval(f"si({arg}={points[i]})")

    ev = P.get_evaluation(points)
    assert cur == ev


if __name__ == "__main__":
    l = 50
    p = 87276363241
    P = Prover(l, p, True)
    verify(P)
