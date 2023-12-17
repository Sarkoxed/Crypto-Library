# https://www.mat.uniroma2.it/~schoof/ctpts.pdf

from division_polynomial import init_cache_noy, psi_cached_noy, phi_cached_noy, omega_cached_noy
from sage.all import var, GF, PolynomialRing, Primes, gcd, randint, prod, crt
from Crypto.Util.number import getPrime

def get_base(q):
    base = []
    prod = 1
    for l in Primes():
        prod *= l
        base.append(l)
        if prod**2 > 16 * q:
            break
    return base

#def get_x_j_psi(x, y_squared, cache, j): # TODO handle y^2
#    psin_1 = psi_cached_noy(abs(j) - 1, cache, y_squared)
#    psin1  = psi_cached_noy(abs(j) + 1, cache, y_squared)
#    psin   = psi_cached_noy(abs(j), cache, y_squared)
#
#    x_j_num = x * psin**2 - psin_1 * psin1
#    x_j_den = psin**2
#    return x_j_num, x_j_den
#
#def get_y_j_div_y_psi(x, y_squared, cache, j): # works
#    psin   = psi_cached_noy(abs(j), cache, y_squared)
#    psin2n = psi_cached_noy(2 * abs(j), cache, y_squared)
#
#    y_j_num = psi2n
#    y_j_den = 2 * psin**4
#    if j < 0:
#        y_j_num = -y_j_num
#    return y_j_num, y_j_den


def get_x_j(x, y_squared, cache, j):
    x_j_num = phi_cached_noy(abs(j), cache, x, y_squared)
    x_j_den = psi_cached_noy(abs(j), cache, y_squared)**2
    if abs(j) % 2 == 0:
        x_j_den *= y_squared
    
    return x_j_num, x_j_den

def get_y_j_div_y(x, y_squared, cache, j):
    y_j_num = omega_cached_noy(abs(j), cache, y_squared)
    y_j_den = psi_cached_noy(abs(j), cache, y_squared)**3
    if j < 0:
        y_j_num = -y_j_num

    if abs(j) % 2 == 0:
        y_j_den *= y_squared**2

    return y_j_num, y_j_den

# (x1, y1) = (x^(p^2), y^(p^2)) + pl * (x, y)
# y^2 = x^3 + A * x + B
# x_pl = phi_pl(x) / psi_pl(x)^2
# y_pl = y * omega_pl(x) / psi_pl(x)^3
#
# x1(x, y) = (y^(p^2) - y_pl)^2 / (x^(p^2) - x_pl)^2 - x_pl - x^(p^2)
# x1(x) = (y^2 * ((y^2)^((p^2 - 1) / 2) - omega_pl(x) / psi_pl(x)^3)^2) / (x^(p^2) - phi_pl(x)/ psi_pl(x)^2)^2 - x^(p^2) - phi_pl(x) / psi_pl(x)^2
#
# x1_num(x) = y^2 * ((y^2)^((p^2-1)/2) * psi_pl(x)^3 - omega_pl(x))^2 - phi_pl(x) * (x^(p^2) * psi_pl(x)^2 - phi_pl(x))^2 - x^(p^2) * psi_pl(x)^2 * (x^(p^2) * psi_pl(x)^2 - phi_pl(x))^2
# x1_den(x) = psi_pl(x)^2 * (x^(p^2) * psi_pl(x)^2 - phi_pl(x))^2
# odd case equations
def get_x1(x, y_squared, cache, q, ql):
    x_ql_num, x_ql_den = get_x_j(x, y_squared, cache, ql)
    
    if not (x_ql_num - x_ql_den * x**(q**2)).is_unit():
        return None, (x_ql_num - x_ql_den * x**(q**2))

    y_ql_num, y_ql_den = get_y_j_div_y(x, y_squared, cache, ql)

    x_q2 = x**(q**2)
    lambda_2_num = y_squared * (y_squared**((q**2 - 1)//2) * y_ql_den - y_ql_num)**2 * x_ql_den**2
    lambda_2_den = y_ql_den**2 * (x_q2 * x_ql_den - x_ql_num)**2
    
    x1_num = lambda_2_num * x_ql_den - x_ql_num * lambda_2_den - x_q2 * lambda_2_den * x_ql_den
    x1_den = lambda_2_den * x_ql_den

    return x1_num, x1_den

# y1 = lambda * (x_pl - x1) - y_pl
#
# y1 = (y^(p^2) - omega(x) / psi(x)^3 * y) / (x^(p^2) - phi(x)/psi(x)^2) * (phi(x) / psi(x)^2 - x1_num / x1_den) - omega(x)/psi(x)^3 * y
# y1 / y = ((y^2)^((p^2-1)//2) * psi(x)^3 - omega(x)) / (x^(p^2) * psi(x)^3 - phi(x) * psi(x)) *  (phi(x) * x1_den - x1_num * psi(x)^2) / (psi(x)^2 * x1_den) - omega(x) / psi(x)^3  
# for n is odd. in even case consider dividing x by y^2 and y by y^4
def get_y1_div_y(x, y_squared, x1_num, x1_den, cache, q, ql):
    x_ql_num, x_ql_den = get_x_j(x, y_squared, cache, ql)
    y_ql_num, y_ql_den = get_y_j_div_y(x, y_squared, cache, ql)

    lambda_num = (y_squared ** ((q**2 - 1)//2) * y_ql_den - y_ql_num) * x_ql_den
    lambda_den = (x**(q**2) * x_ql_den - x_ql_num) * y_ql_den

    left_num = lambda_num * (x_ql_num * x1_den - x1_num * x_ql_den)
    left_den = lambda_den * (x_ql_den * x1_den)

    y1_num = left_num * y_ql_den - left_den * y_ql_num
    y1_den = left_den * y_ql_den

    return y1_num, y1_den

def trace_mod_2(A, B, P, x):
    q = P.base_ring().order()
    mod = P(x**3 + A * x + B)
    Q = P.quotient(mod)
    left = Q(x)**q - Q(x)
    if left.is_unit():
        return 1
    return 0

def trace_mod_l(A, B, P, x, y_squared, l, cache_l):
    q = P.base_ring().order()
    ql = q % l
    if 2 * ql > l:
        ql = ql - l
    
    psi_l = psi_cached_noy(l, cache_l, y_squared)
    Q = P.quotient_ring(psi_l)
    cache = init_cache_noy(A, B, Q(x))
    
    x1_num, x1_den = get_x1(Q(x), Q(y_squared), cache, q, ql)
    
    if x1_num is not None:
        for j in range(1, (l-1)//2 + 1):
            x_j_num, x_j_den = get_x_j(Q(x), Q(y_squared), cache, j)
            x_q_j_num = x_j_num**q
            x_q_j_den = x_j_den**q
        
            x1_x_j = x1_num * x_q_j_den - x_q_j_num * x1_den 
            # x1 - x^q_j == 0? (x1, y1) == j (x^p, +-y^p) ? 
            if x1_x_j == 0:
                y_j_num, y_j_den = get_y_j_div_y(Q(x), Q(y_squared), cache, j)
                # need extra argument for (r2(x) * y)^p cache, j)
                y_q_j_num = y_j_num**q * Q(y_squared)**((q - 1)//2) 
                y_q_j_den = y_j_den**q
        
                y1_num, y1_den = get_y1_div_y(Q(x), Q(y_squared), x1_num, x1_den, cache, q, ql)
        
                y1_y_j_div_y = y1_num * y_q_j_den - y1_den * y_q_j_num
                if y1_y_j_div_y == 0:
                    return j
                else:
                    return l-j
        else:
            raise ValueError

    ql = GF(l)(q)
    if not ql.is_square():
        return 0
    
    w = ql.sqrt()
    x_w_num, x_w_den = get_x_j(Q(x), Q(y_squared), cache, int(w))
    
    x_q_x_w = Q(x)**q * x_w_den - x_w_num
    if x_q_x_w.is_unit():
        return 0
    
    y_w_num, y_w_den = get_y_j_div_y(Q(x), Q(y_squared), cache, int(w))
    y_q_div_y = Q(y_squared)**((q - 1)//2)
        
    y_q_y_w_div_y = y_q_div_y * y_w_den - y_w_num
    if y_q_y_w_div_y.is_unit():
        return int(-2 * w)
    return int(2 * w)

def get_order(A, B, q):
    base = get_base(q)
    
    x = var('x')
    P = PolynomialRing(GF(q), x)
    y_squared = P(x**3 + A * x + B)
    al = []
    cache_l = init_cache_noy(A, B, P(x))

    for l in base:
        if l == 2:
            al.append(trace_mod_2(A, B, P, x))
        else:
            al.append(trace_mod_l(A, B, P, P(x), y_squared, l, cache_l))
    #print(f"{base=}")
    #print(f"{al =}")       
    a = int(crt(al, base))
    mod = prod(base)
    
    while a**2 > 4 * q:
        a -= mod
    #print(a)
    return q + 1 - a
