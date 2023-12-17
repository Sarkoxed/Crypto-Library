def psi(a, b, x, n, y): # too slow
    if n == 0:
        return 0
    elif n == 1:
        return 1
    elif n == 2:
        return 2 * y
    elif n == 3:
        return 3 * x**4 + 6 * a * x**2 + 12 * b * x - a**2
    elif n == 4:
        return 4 * y * (x**6 + 5 * a * x**4 + 20 * b* x**3 - 5 * a**2 * x**2 - 4 * a * b * x - 8 * b**2 - a**3)

    m = n >> 1
    if n & 1:
        psim2 =  psi(a, b, x, m + 2, y)
        psim1 =  psi(a, b, x, m + 1, y)
        psim =   psi(a, b, x, m, y)
        psim_1 = psi(a, b, x, m - 1, y)
        return psim2 * psim**3 - psim_1 * psim1**3
    else:
        psim2 =  psi(a, b, x, m + 2, y)
        psim1 =  psi(a, b, x, m + 1, y)
        psim =   psi(a, b, x, m, y)
        psim_1 = psi(a, b, x, m - 1, y)
        psim_2 = psi(a, b, x, m - 2, y)

        return psim * pow(2 * y, -1) * (psim2 * psim_1**2 - psim_2 *psim1**2)


def phi(a, b, x, n, y): # too slow
    psin1 =  psi(a, b, x, n+1, y)
    psin =   psi(a, b, x, n, y)
    psin_1 = psi(a, b, x, n-1, y)
    return x * psin**2 - psin1 * psin_1


def omega(a, b, x, n, y): # too slow
    if n == 1:
        return y
    psin2 =  psi(a, b, x, n + 2, y)
    psin1 =  psi(a, b, x, n + 1, y)
    psin_1 = psi(a, b, x, n - 1, y)
    psin_2 = psi(a, b, x, n - 2, y)
    return (psin2 * psin_1**2 - psin_2 * psin1**2) * pow(4 * y, -1)






# optimized part

def init_cache(a, b, x, y):
    Q = x.parent()
    tmp = dict()
    tmp[0] = Q(0)
    tmp[1] = Q(1)
    tmp[2] = Q(2 * y)
    tmp[3] = 3 * x**4 + 6 * a * x**2 + 12 * b * x - a**2
    tmp[4] = 4 * y * (x**6 + 5 * a * x**4 + 20 * b* x**3 - 5 * a**2 * x**2 - 4 * a * b * x - 8 * b**2 - a**3)
    return tmp

# same as e.division_polynomial(m = n, two_torsion_multiplicity=1)
def psi_cached(n, cache, y):
    if n in cache:
        return cache[n]
    
    m = n >> 1
    if n & 1:
        psim2 =  psi_cached(m + 2, cache, y)
        psim1 =  psi_cached(m + 1, cache, y)
        psim =   psi_cached(m, cache, y)
        psim_1 = psi_cached(m - 1, cache, y)
        cache[n] = psim2 * psim**3 - psim_1 * psim1**3
    else:
        psim2 =  psi_cached(m + 2, cache, y)
        psim1 =  psi_cached(m + 1, cache, y)
        psim =   psi_cached(m, cache, y)
        psim_1 = psi_cached(m - 1, cache, y)
        psim_2 = psi_cached(m - 2, cache, y)
    
        cache[n] = psim * pow(2 * y, -1) * (psim2 * psim_1**2 - psim_2 *psim1**2)
        if len(cache) % 4000 == 0:
            print(len(cache))
    
    return cache[n]

def phi_cached(n, cache, x, y):
    psin1 =  psi_cached(n+1, cache, y)
    psin =   psi_cached(n,   cache, y)
    psin_1 = psi_cached(n-1, cache, y)
    return x * psin**2 - psin1 * psin_1

def omega_cached(n, cache, y):
    if n == 1:
        return y
    psin2 =  psi_cached(n + 2, cache,  y)
    psin1 =  psi_cached(n + 1, cache, y)
    psin_1 = psi_cached(n - 1, cache, y)
    psin_2 = psi_cached(n - 2, cache, y)
    return (psin2 * psin_1**2 - psin_2 * psin1**2) / (4 * y)




# When we do not know y; for example in rings of unknown order

def init_cache_noy(a, b, x):
    Q = x.parent()
    tmp = dict()
    tmp[0] = Q(0)
    tmp[1] = Q(1)
    tmp[2] = Q(2)
    tmp[3] = 3 * x**4 + 6 * a * x**2 + 12 * b * x - a**2
    tmp[4] = 4 * (x**6 + 5 * a * x**4 + 20 * b* x**3 - 5 * a**2 * x**2 - 4 * a * b * x - 8 * b**2 - a**3)
    return tmp
 
# same as e.division_polynomial(m = n, two_torsion_multiplicity=0) * 2(n % 2 = 0)
def psi_cached_noy(n, cache, y_squared):
    if n in cache:
        return cache[n]

    m = n >> 1
    if n & 1:
        psim2 =  psi_cached_noy(m + 2, cache, y_squared)
        psim1 =  psi_cached_noy(m + 1, cache, y_squared)
        psim =   psi_cached_noy(m, cache, y_squared)
        psim_1 = psi_cached_noy(m - 1, cache, y_squared)

        if m & 1:
            cache[n] = psim2 * psim**3 - y_squared**2 * psim_1 * psim1**3
        else:
            cache[n] = y_squared**2 * psim2 * psim**3 - psim_1 * psim1**3

    else:
        psim2 =  psi_cached_noy(m + 2, cache, y_squared)
        psim1 =  psi_cached_noy(m + 1, cache, y_squared)
        psim =   psi_cached_noy(m, cache, y_squared)
        psim_1 = psi_cached_noy(m - 1, cache, y_squared)
        psim_2 = psi_cached_noy(m - 2, cache, y_squared)
        
        cache[n] = psim * (psim2 * psim_1**2 - psim_2 *psim1**2) / 2

        if len(cache) % 4000 == 0:
            print(len(cache))
    
    return cache[n]

def phi_cached_noy(n, cache, x, y_squared):
    psin1 =  psi_cached_noy(n+1, cache, y_squared)
    psin =   psi_cached_noy(n,   cache, y_squared)
    psin_1 = psi_cached_noy(n-1, cache, y_squared)
    if n % 2 == 0:
        return x * psin**2 * y_squared - psin1 * psin_1
    else:
        return x * psin**2 - y_squared * psin1 * psin_1

def omega_cached_noy(n, cache, y_squared):
    if n == 1:
        return cache[1]
    psin2 =  psi_cached_noy(n + 2, cache,  y_squared)
    psin1 =  psi_cached_noy(n + 1, cache, y_squared)
    psin_1 = psi_cached_noy(n - 1, cache, y_squared)
    psin_2 = psi_cached_noy(n - 2, cache, y_squared)

    return (psin2 * psin_1**2 - psin_2 * psin1**2) / 4
