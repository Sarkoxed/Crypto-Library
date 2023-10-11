from Crypto.Util.number import isPrime
class Montgomery:
    p = 0
    b = 0
    a = 0

    def __init__(self, p, b, a):
        if (b * (a**2 - 4)) % p == 0:
            raise Exception("kal")

        self.p = p
        self.a = a % p
        self.b = b % p

    def is_on_curve(self, x, y):
        return (self.b * y**2) % self.p == (x**3 + self.a * x**2 + x) % self.p

class MPoint:
    x = 0
    y = 1
    E = None
    
    def __init__(self, x, y, E):
        if not E.is_on_curve(x, y) and x != 0 and y != 1:
            raise Exception("not on curve")
        
        self.x = x % E.p
        self.y = y % E.p
        self.E = E
        
    def is_infinity(self):
        return self.x == 0 and self.y == 1

    def __add__(self, Q):
        if Q.E != self.E:
            raise Exceptino("Incompatible curves")

        if self.is_infinity():
            return Q

        elif Q.is_infinity():
            return self
        
        elif self.x == Q.x and self.y == self.E.p - Q.y:
            return MPoint(0, 1, self.E)
        
        x1, y1 = self.x, self.y
        x2, y2 = Q.x, Q.y
        
        l = 0
        if self.x != Q.x:
            l = ((y2 - y1) * pow(x2 - x1, -1, self.E.p)) % self.E.p
        else:
            l = ((3 * x1**2 + 2 * self.E.a * x1 + 1) * pow(2 * self.E.b * y1, -1, self.E.p)) % self.E.p

        x3 = (self.E.b * l**2 - self.E.a - x1 - x2) % self.E.p
        y3 = ((2 *  x1 + x2 + self.E.a) * l - self.E.b * l**3 - y1) % self.E.p

        return MPoint(x3, y3, self.E)
    
    def __neg__(self):
        return MPoint(self.x, -self.y, self.E)
    
    def __sub__(self, Q):
        return self + (-Q)
    
    def __mul__(self, n: int):
        if n == 0:
            return MPoint(0, 1, self.E)

        if n < 0:
            self = -self
            n = -n

        r = MPoint(0, 1, self.E)
        q = self
        while n:
            if n & 1:
                r = r + q
            q = q + q
            n >>= 1
        return r

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
    
    def __repr__(self):
        return f"({self.x}, {self.y})"

#p = 2**255 - 19
#a = -1
#c = 1
#d = 0x52036cee2b6ffe738cc740797779e89800700a4d4141d8ab75eb4dca135978a3
#n = 0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3ed
#E = Edwards(p, a, d, c)
#G = Point(0x216936d3cd6e53fec0a4e231fdd6dc5c692cc7609525a7b2c9562d608f25d51a, 0x6666666666666666666666666666666666666666666666666666666666666658, E)
#
#print(G * n)
#print(G.constant_time_mul(n))
