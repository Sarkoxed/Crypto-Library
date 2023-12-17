from sage.all import RR, GF, oo


class EC:
    _a1, _a2, _a3, _a4, _a6 = [0] * 5
    _K = RR

    def __init__(self, a1=0, a2=0, a3=0, a4=0, a6=0, K=RR):
        self._K = K
        self._a1, self._a2, self._a3, self._a4, self._a6 = (
            K(a1),
            K(a2),
            K(a3),
            K(a4),
            K(a6),
        )
        if self.is_singular():
            raise Exception("Singular Curve")

    def tup(self):
        return (self._a1, self._a2, self._a3, self._a4, self._a6)

    def is_singular(self):
        a1, a2, a3, a4, a6 = self._a1, self._a2, self._a3, self._a4, self._a6
        b2 = a1**2 + 4 * a2
        b4 = 2 * a4 + a1 * a3
        b6 = a3**2 + 4 * a6
        b8 = a1**2 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3**2 - a4**2

        det = -(b2**2) * b8 - 8 * b4**3 - 27 * b6**2 + 9 * b2 * b4 * b6
        return det == 0

    def __call__(self, t: tuple):
        x, y, z = self._K(t[0]), self._K(t[1]), self._K(t[2])
        a1, a2, a3, a4, a6 = self.tup()

        p = ECPoint(x, y, z, self)
        if not self.isonCurve(p):
            return None
        return p

    def isonCurve(self, P):
        if P.is_infinity():
            return True

        x, y = P._x, P._y
        a1, a2, a3, a4, a6 = P._EC.tup()
        return y**2 + a1 * x * y + a3 * y == x**3 + a2 * x**2 + a4 * x + a6

    def naive_point_counter(self):
        res = [ECPoint(0, 1, 0, self)]

        for i in range(self._K.order()):
            for j in range(self._K.order()):
                p = self((i, j, 1))
                if not p is None:
                    res.append(p)
        return res, len(res)

    def random_point(self):
        K = self._K
        while True:
            i = K.random_element()
            y_coord_sq = K(i**3 + self._a4 * i + self._a6)
            leg_sym = y_coord_sq ** ((K.order() - 1) // 2)

            if leg_sym == 1:
                y = K(y_coord_sq).sqrt()
                P = ECPoint(i, y, 1, self)
                return P

    @staticmethod
    def rec_ord(a, b, p, n):
        if n == 1:
            return a + b
        elif n == 2:
            return a**2 + b**2

        t0 = a + b
        t1 = p

        a, b = 2, t0
        for i in range(n - 1):
            a, b = b, t0 * b - p * a
        return b

    @staticmethod
    def power_ord(a, b, n):
        return a**n + b**n

    def get_order(self, P):
        n = self._K.degree()
        p = self._K.base().order()
        e = EC(*self.tup(), K=GF(p))
        e0 = e.get_naive_order(ECPoint(0, 1, 0, GF(p)))
        t = p + 1 - e0
        a, b = (t + sqrt(t**2 - 4 * p)) / 2, (t - sqrt(t**2 - 4 * p)) / 2
        tn1 = self.rec_ord(a, b, p, n)
        tn2 = self.power_ord(a, b, n)
        assert tn1 == tn2
        return tn1 + 1 + p**n


class ECPoint:
    _x, _y, _z = 0, 0, 0
    _EC = None

    def __init__(self, x, y, z, E: EC):
        self._x, self._y, self._z = x, y, z
        self._EC = E

    def x(self):
        return self._x

    def y(self):
        return self._y

    def is_infinity(self):
        return self._z == 0

    def __neg__(self):
        if not (self.is_infinity()):
            x, y = (self._x, -self._y - self._EC._a1 * self._x - self._EC._a3)
            return ECPoint(x, y, 1, self._EC)

    def __add__(self, Q):
        if self.is_infinity():
            return Q
        elif Q.is_infinity():
            return self
        if Q == -self:
            return ECPoint(0, 1, 0, self._EC)

        a1, a2, a3, a4, a6 = self._EC.tup()

        if self != Q:
            l = (Q._y - self._y) / (Q._x - self._x)
            nu = ((self._y * Q._x) - (self._x * Q._y)) / (Q._x - self._x)
        else:
            l = (3 * self._x * self._x + 2 * a2 * self._x + a4 - a1 * self._y) / (
                2 * self._y + a1 * self._x + a3
            )
            nu = (
                -self._x * self._x * self._x + a4 * self._x + 2 * a6 - a3 * self._y
            ) / (2 * self._y + a1 * self._x + a3)

        x3 = l * l + a1 * l - a2 - self._x - Q._x
        y3 = -(l + a1) * x3 - nu - a3
        return ECPoint(x3, y3, 1, self._EC)

    def __sub__(self, Q):
        Q = -Q
        return self + Q

    #    def double_and_add(self, n: int):
    #        if(n < 0):
    #            self = -self
    #            n = -n
    #        if(n == 0):
    #            return ECPoint(0,1,0, self._EC)
    #        Q = ECPoint(0, 1, 0, self._EC)
    #        while(n > 1):
    #            if(n & 1):
    #                Q = self + Q
    #                self = self + self
    #                n = (n-1)//2
    #            else:
    #                self = self + self
    #                n //= 2
    #        #print(P, Q, n)
    #        return self + Q

    @staticmethod
    def ternary(n):
        n += [0]
        j, k = 0, 0
        for i in range(len(n)):
            if n[i] == 1:
                k += 1
                if k == 2:
                    n[i - 1] = -1
                    n[i] = 0
                elif k > 2:
                    n[i] = 0

            else:
                j = i + 1
                if k > 1:
                    n[i] = 1
                k = 0
        if n[-1] == 0:
            n = n[:-1]
        return n

    def __mul__(self, n: int):
        if n == 0:
            return ECPoint(0, 1, 0, self._EC)
        if n < 0:
            self = -self
            n = -n
        n = self.ternary(n)
        q = ECPoint(0, 1, 0, self._EC)
        for i in range(len(n)):
            if n[i] == -1:
                q = q - self
                self = self + self
            elif n[i] == 1:
                q = q + self
                self = self + self
            else:
                self = self + self
        return q

    __rmul__ = __mul__

    def constant_time_mul(self, n: int):
        n = [int(x) for x in bin(n)[2:][::-1]]
        R0, R1 = self, self + self
        for i in range(len(n) - 2, -1, -1):
            if n[i] == 0:
                R0, R1 = R0 + R0, R0 + R1
            else:
                R0, R1 = R0 + R1, R1 + R1
        return R0

    def naive_ecdlp(self, Q) -> int:
        n = self._EC.get_naive_order(self)
        print(n)
        for i in range(n):
            if i * self == Q:
                return i
        return None

    def __str__(self):
        return f"({self._x}:{self._y}:{self._z})"

    def __tuple__(self):
        return (self._x, self._y, self._z)

    def __list__(self):
        return list(tuple(self))


if __name__ == "__main__":
    print(1)
