# https://eprint.iacr.org/2017/212.pdf

from sage.all import GF, EllipticCurve, PolynomialRing, sqrt, floor


# Curves of the form B*y^2 = x^3 + A * x^2 + x
class Montgomery:
    order = None

    def __init__(self, A: int, B: int, p: int):
        if B % p == 0 or pow(A, 2, p) == 4:
            raise ValueError("Singular curve encountered")

        self.G = GF(p)
        self.A = self.G(A)
        self.B = self.G(B)

    def to_weierstrass(self, P=None):
        assert self.is_on_curve(P.x, P.y)
        a = self.B**2 * (1 - self.A**2 / 3)
        b = self.B**3 * self.A / 3 * (2 * self.A**2 / 9 - 1)
        E = EllipticCurve(self.G, [a, b])
        if P is None:
            return E

        u = self.B * (P.x + self.A / 3)
        v = self.B**2 * P.y
        return E((u, v))

    def order_lame(self) -> int:
        if self.order is None:
            self.order = self.to_weierstrass().order()
        return self.order

    def random_point(self):
        while True:
            x = self.G.random_element()
            y2 = (x**3 + self.A * x**2 + x) * pow(self.B, -1)
            if y2.is_square():
                return AffineMontgomeryPoint(self, x, y2.sqrt())

    def is_on_curve(self, x, y) -> bool:
        x = self.G(x)
        y = self.G(y)
        return self.B * y**2 == x**3 + self.A * x**2 + x


class AffineMontgomeryPoint:
    order = None

    def __init__(
        self, curve: Montgomery, x: int = None, y: int = None, is_inf: bool = None
    ):
        if is_inf:
            self.curve = curve
            self.x = self.curve.G(0)
            self.y = self.curve.G(1)
            self.z = self.curve.G(0)
            return

        if not curve.is_on_curve(x, y):
            raise ValueError("InvalidPoint")

        self.curve = curve
        self.x = self.curve.G(x)
        self.y = self.curve.G(y)
        self.z = self.curve.G(1)

    def __eq__(self, P):
        if self.is_inf():
            return P.is_inf()

        return P.x == self.x and P.y == self.y and P.z == self.z

    def is_inf(self):
        return self.z == 0

    def __neg__(self):
        return AffineMontgomeryPoint(self.curve, self.x, -self.y)

    def __add__(self, Q):
        if Q.is_inf():
            return self

        if self.is_inf():
            return Q

        if self.curve != Q.curve:
            raise ValueError("Curves do not match")

        if self.x == Q.x and self.y == -Q.y:
            return AffineMontgomeryPoint(self.curve, is_inf=True)

        l = 0
        if self != Q:
            l = (Q.y - self.y) / (Q.x - self.x)
        else:
            if self.y == 0:
                return AffineMontgomeryPoint(self.curve, is_inf=True)

            l = (3 * self.x**2 + 2 * self.curve.A * self.x + 1) / (
                2 * self.curve.B * self.y
            )

        new_x = self.curve.B * l**2 - (self.x + Q.x) - self.curve.A
        new_y = l * (self.x - new_x) - self.y
        return AffineMontgomeryPoint(self.curve, new_x, new_y)

    def __sub__(self, Q):
        return self + (-Q)

    def __mul__(self, n: int):
        if n < 0:
            return (-n) * (-self)
        elif n == 0:
            return AffineMontgomeryPoint(self.curve, is_inf=True)

        R0, R1 = self, self + self
        for k in bin(n)[3:]:
            if k == "0":
                R0, R1 = R0 + R0, R0 + R1
            else:
                R0, R1 = R0 + R1, R1 + R1
        return R0

    def __rmul__(self, n: int):
        return self * n

    def order_lame(self):
        if self.order is None:
            self.order = self.curve.to_weierstrass(self).order()
        return self.order

    def __repr__(self):
        return f"({self.x} : {self.y} : {self.z})"


class ProjectiveMontgomeryPoint:
    def __init__(self, curve: Montgomery, x: int = None, z: int = None):
        self.curve = curve
        if z == 0:
            self.x = self.curve.G(1)
            self.z = self.curve.G(0)
        else:
            self.x = self.curve.G(x)
            self.z = self.curve.G(z)

    @staticmethod
    def from_affine(P):
        return ProjectiveMontgomeryPoint(P.curve, P.x, P.z)

    def is_inf(self):
        return self.z == 0

    def normalize(self):
        if self.z != 0:
            self.x *= pow(self.z, -1)
            self.z = self.curve.G(1)

    def __eq__(self, P):
        if self.is_inf():
            return P.is_inf()

        return self.x * P.z == P.x * self.z

    # pseuso Add
    # X+ = X_ * ((Xp - Zp)(Xq + Zq) + (Xp + Zp)(Xq - Zq))^2
    # Z+ = Z_ * ((Xp - Zp)(Xq + Zq) - (Xp + Zp)(Xq - Zq))^2
    @staticmethod
    def xADD(P, Q, P_Q):
        assert P.curve == Q.curve and P.curve == P_Q.curve
        v0 = P.x + P.z
        v1 = Q.x - Q.z
        v1 = v0 * v1

        v0 = P.x - P.z
        v2 = Q.x + Q.z
        v2 = v2 * v0

        v3 = v1 + v2
        v3 = v3 * v3

        v4 = v1 - v2
        v4 = v4 * v4

        x = P_Q.z * v3
        z = P_Q.x * v4
        return ProjectiveMontgomeryPoint(P.curve, x, z)

    # pseudo Dbl
    # X2p = (Xp + Zp)^2 (Xp - Zp)^2
    # Z2p = (4XpZp)((Xp - Zp)^2 + ((A+2)/4)(4XpZp))
    @staticmethod
    def xDBL(P):
        v1 = P.x + P.z
        v1 = v1 * v1

        v2 = P.x - P.z
        v2 = v2 * v2

        x = v1 * v2

        v1 = v1 - v2
        v3 = ((P.curve.A + 2) / 4) * v1
        v3 = v3 + v2

        z = v1 * v3
        return ProjectiveMontgomeryPoint(P.curve, x, z)

    # Montgomery Ladder
    @staticmethod
    def scalarmul(P, n, recovery: bool = False):
        if n < 0:
            # TODO: maybe lift it, get the order and reduce mod
            raise ValueError("Not implemented")

        if n == 0:
            return ProjectiveMontgomeryPoint(P.curve, z=0)

        xDBL = ProjectiveMontgomeryPoint.xDBL
        xADD = ProjectiveMontgomeryPoint.xADD

        x0, x1 = P, xDBL(P)
        for k in bin(n)[3:]:
            if k == "0":
                x0, x1 = xDBL(x0), xADD(x0, x1, P)
            else:
                x0, x1 = xADD(x0, x1, P), xDBL(x1)

        if recovery:
            return x0, x1
        return x0

    # Don't know, seems like (1-b) * P + b * Q should work too
    @staticmethod
    def constant_time_swap(b, P, Q):
        n = P.curve.G.characteristic().bit_length()
        b = (1 << (n + 1)) - b

        y0 = int(P.x) ^ int(Q.x)
        y1 = int(P.z) ^ int(Q.z)

        # should not be short circuited, didn't check
        v0 = b & y0
        v1 = b & y1

        P_ = ProjectiveMontgomeryPoint(P.curve, v0 ^ int(P.x), v1 ^ int(P.z))
        Q_ = ProjectiveMontgomeryPoint(P.curve, v0 ^ int(Q.x), v1 ^ int(Q.z))

        return P_, Q_

    @staticmethod
    def uniform_ladder(P, n, recovery=False):
        if n == 0:
            return
        xDBL = ProjectiveMontgomeryPoint.xDBL
        xADD = ProjectiveMontgomeryPoint.xADD
        swap = ProjectiveMontgomeryPoint.constant_time_swap

        x0, x1 = xDBL(P), P
        k = [int(x) for x in bin(n)[2:]][::-1]
        for i in reversed(range(len(k) - 1)):
            x0, x1 = swap(k[i + 1] ^ k[i], x0, x1)
            x0, x1 = xDBL(x0), xADD(x0, x1, P)
        x0, x1 = swap(k[0], x0, x1)

        if recovery:
            return x0, x1
        return x0

    # P: Affine
    # Q, P_Q: Projective
    @staticmethod
    def recover(P: AffineMontgomeryPoint, Q, P_Q):
        if (2 * P).is_inf():
            raise ValueError("Got 2-torsion point P")

        if Q == ProjectiveMontgomeryPoint.from_affine(P):
            raise VlaueError("Got same projective points")

        v1 = P.x * Q.z

        v2 = Q.x + v1
        v3 = Q.x - v1

        v3 = v3 * v3
        v3 = v3 * P_Q.x

        v1 = 2 * P.curve.A * Q.z
        v2 = v2 + v1

        v4 = P.x * Q.x
        v4 = v4 + Q.z

        v2 = v2 * v4
        v1 = v1 * Q.z
        v2 = v2 - v1
        v2 = v2 * P_Q.z

        Y = v2 - v3

        v1 = 2 * P.curve.B * P.y
        v1 = v1 * Q.z
        v1 = v1 * P_Q.z

        X = v1 * Q.x
        Z = v1 * Q.z

        if Z == 0:
            return AffineMontgomeryPoint(P.curve, is_inf=True)

        X /= Z
        Y /= Z
        return AffineMontgomeryPoint(P.curve, X, Y)

    def EUCLID2D(P, Q, P_Q, m, n):
        xDBL = ProjectiveMontgomeryPoint.xDBL
        xADD = ProjectiveMontgomeryPoint.xADD

        s0, s1 = m, n
        x0, x1, x_ = P, Q, P_Q

        while s0 != 0:
            if s1 < s0:
                s0, s1 = s1, s0
                x0, x1, x_ = x1, x0, x_
            elif s1 <= 4 * s0:
                s0, s1 = s0, s1 - s0
                x0, x1, x_ = xADD(x1, x0, x_), x1, x0
            elif s0 % 2 == s1 % 2:
                s0, s1 = s0, (s1 - s0) // 2
                x0, x1, x_ = xADD(x1, x0, x_), xDBL(x1), x_
            elif s1 % 2 == 0:
                s0, s1 = s0, s1 // 2
                x0, x1, x_ = x0, xDBL(x1), xADD(x1, x_, x0)
            else:
                s0, s1 = s0 // 2, s1
                x0, x1, x_ = xDBL(x0), x1, xADD(x0, x_, x1)

        while s1 % 2 == 0:
            s1, x1 = s1 // 2, xDBL(x1)

        if s1 > 1:
            x1 = ProjectiveMontgomeryPoint.scalarmul(x1, s1)

        return x1

    def euclidian_pseudoscalar(P, n):
        if n == 0:
            return ProjectiveMontgomeryPoint(P.curve, z=0)

        n = n if n > 0 else -n

        s, x = n, P
        while s % 2 == 0:
            s, x = s // 2, ProjectiveMontgomeryPoint.xDBL(x)

        phi = (1 + sqrt(5)) / 2
        r = floor(s / phi)

        # Was not working with 0 like in paper
        x0, x1 = x, x
        m, n = r, s - r
        if r % 2 == 0:
            x0 = ProjectiveMontgomeryPoint.xDBL(x0)
            m //= 2
        else:
            x1 = ProjectiveMontgomeryPoint.xDBL(x1)
            n //= 2
        x = ProjectiveMontgomeryPoint.EUCLID2D(x0, x1, x, m, n)
        return x

    def __repr__(self):
        return f"({self.x} : {self.z})"
