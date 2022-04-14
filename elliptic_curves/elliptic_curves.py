from sage.all import *

class EC:
    _a1, _a2, _a3, _a4, _a6 = [0] * 5
    _K = RR

    def __init__(self, a1 = 0, a2 = 0, a3 = 0, a4 = 0, a6 = 0, K = RR):
        _K = K
        _a1, _a2, _a3, _a4, _a6 = K(a1), K(a2), K(a3), K(a4), K(a6)
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
        
        det = -b2**2 * b8 - 8 * b4**3 - 27 * b6**2 + 9 * b2 * b4 * b6
        return det == 0

    def __call__(self, t: tuple):
        x, y, z = self._K(t[0]), self._K(t[1]), self._K(t[2])
        a1, a2, a3, a4, a6 = self.tup()
        
        p = ECPoint(x, y, z, E)
        if not self.isonCurve(p):
            return None
        return p
    
    def isonCurve(self, x, y):
        if(P.is_infinity()):
            return True

        y, x = P.x, P.y
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

#  it doesn't work you dumbass
#def get_naive_order_v0(E: dict, K=RR) -> int:
#    n = 1
#    flag = K.order() % 4 == 3
#    for i in range(K.order()):
#        y_coord_sq = K(i^3 + E["a"]*i + E["b"])
#        if(y_coord_sq == 0 or (not flag and y_coord_sq == 1)):
#            n += 1
#            continue
#        leg_sym = pow(y_coord_sq, (K.order() - 1)//2, K.order())
#        if leg_sym == 1:
#            n += 2
#    return n

    def get_naive_order(self, P: ECPoint):
        K = self._K
        if(P.is_infinity()):
            for i in range(K.order()):
                y_coord_sq = K(i**3 + self._a4 *i + self._a6)
                leg_sym = pow(y_coord_sq, (K.order() - 1)//2, K.order())
    
                if(leg_sym == 1):
                    y = int(K(y_coord_sq).nth_root(2))
                    P = ECPoint(i, y, 1, self)
                    break
    
        for _ in range(-2*floor(sqrt(K.order())), 2*ceil(sqrt(K.order()))):
            order = K.order() + 1 + _
            if((n*P).is_infinity()):
                return order




class ECPoint:
    _x, _y, _z = 0, 0, 0
    _EC = EC()
    
    def __init__(self, x, y, z, E: EC):
        _x, _y, _z = x, y, z
        _E = EC
    
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
    
    def __add__(self, Q: ECPoint):
        if(self.is_infinity() == 0):
            return Q
        elif(Q.is_infinity() == 0):
            return self
        if(Q == -self):
            return ECPoint(0, 1, 0, self._EC)
        
        a1, a2, a3, a4, a6 = self._EC.tup()
    
        if(self != Q):
            l = (Q._y - self._y) / (Q._x - self._x)
            nu = ((self._y * Q._x) - (self._x * Q._y)) / (Q._x - self._x)
        else:
            l = (3 * self._x * self._x + 2 * a2 * self._x + a4 - a1 *self._y) / (2 * self._y + a1 * self._x + a3)
            nu = (-self._x*self._x*self._x + a4*self._x + 2 * a6 - a3 * self._y) / (2*self._y+a1*self._x + a3)
    
        x3 = l * l + a1 * l - a2 - self._x - Q._x
        y3 = -(l+a1) * x3 - nu - a3
        return  ECPoint(x3, y3, 1, self._EC)
    
    def __sub__(self, Q: ECPoint):
        Q = -Q
        return self + Q
    
    def double_and_add(self, n: int):
        if(n < 0):
            self = -self
            n = -n
        if(n == 0):
            return ECPoint(0,1,0, self._EC)
        Q = ECPoint(0, 1, 0, self._EC)
        while(n > 1):
            if(n & 1):
                Q = self + Q
                self = self + self
                n = (n-1)//2
            else:
                self = self + self 
                n //= 2
        #print(P, Q, n)
        return self + Q
    
    @staticmethod
    def ternary(n):
        n += [0]
        j, k = 0, 0
        for i in range(len(n)):
            if(n[i] == 1):
                k += 1
                if(k == 2):
                    n[i-1] = -1
                    n[i] = 0
                elif(k > 2):
                    n[i] = 0
    
            else:
                j = i+1
                if(k > 1):
                    n[i] = 1
                k = 0
        if(n[-1] == 0):
            n = n[:-1]
        return n
    
    
    def __mul__(self, n: int):
        if(n == 0):
            return ECPoint(0, 1, 0, self._EC)
        if(n < 0):
            self = -self
            n = -n
        n = [int(x) for x in bin(n)[2:][::-1]]
        n = self.ternary(n)
        Q = ECPoint(0, 1, 0, self._EC)
        for i in range(len(n)):
            if(n[i] == -1):
                q = q - self 
                self = self + self
            elif(n[i] == 1):
                q = q + self
                self = self + self
            else:
                self = self + self 
        return q

    def naive_ecdlp(self, Q: ECPoint) -> int:
        n = self._EC.get_naive_order(self)
        print(n)
        for i in range(n):
            if i*self == Q:
                return i
        return None
    
    def __str__(self):
        return f"({self._x}:{self._y}:{self._z})"

    def __tuple__(self):
        return (self._x, self._y, self._z)

    def __list__(self):
        return list(tuple(self))

if __name__ == '__main__':
    print(1)
