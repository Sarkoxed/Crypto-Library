from sage.all import EllipticCurve, GF

def ternary_expansion(n):
    n = [int(x) for x in bin(n)[2:]]
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

def ternary(P, n):
    if n == 0:
        return P * 0

    if n < 0:
        P = -P
        n = -n

    q = 0
    for i in ternary_expansion(n):
        if i == -1:
            q = q - P
            P = P + P
        elif i == 1:
            q = q + P
            P = P + P
        else:
            P = P + P
    return q

def constant_time(P, n):
    R0, R1 = P, P + P
    for i in bin(n)[3:]:
        if n[i] == "0":
            R0, R1 = R0 + R0, R0 + R1
        else:
            R0, R1 = R0 + R1, R1 + R1
    return R0

# TODO: doesn't work
def get_tau_expansion(ac, c, q, g=1):
    cs = [c] + [0 for _ in range(2*g - 1)]
    rs = []

    i = 0
    while any(cs):
        print(i)
        if cs[0] % q**g == 0:
            ri = 0
        else:
            if q % 2 == 0 and abs(cs[0]) == q**g // 2:
                ri = cs[0]
            else:
                ri = cs[0] % q**g
                if ri > q**g//2:
                    ri -= q**g
        rs.append(ri)
        d = (cs[0] - ri) // q**g
        for j in range(g):
            cs[j] = cs[j + 1] - ac[j + 1] * q**(g - j - 1) * d

        for j in range(g-1):
            cs[g + j] = c[g+j+1] - ac[g - j - 1] * d
        cs[-1] = -d
        i += 1
        #print(cs)
    return rs       

def tau_expansion(P, n):
    e = P.curve()
    a = e.trace_of_frobenius()
