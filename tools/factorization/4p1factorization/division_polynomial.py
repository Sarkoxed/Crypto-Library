# TODO: why e.division_polynomial() is not the same in sage
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
    psin2 =  psi(a, b, x, n + 2, y)
    psin1 =  psi(a, b, x, n + 1, y)
    psin_1 = psi(a, b, x, n - 1, y)
    psin_2 = psi(a, b, x, n - 2, y)
    return (psin2 * psin_1**2 - psin_2 * psin1**2) * pow(4 * y, -1)






# optimized part

def init_cache(a, b, x, y):
    tmp = dict()
    tmp[0] = 0
    tmp[1] = 1
    tmp[2] = 2 * y
    tmp[3] = 3 * x**4 + 6 * a * x**2 + 12 * b * x - a**2
    tmp[4] = 4 * y * (x**6 + 5 * a * x**4 + 20 * b* x**3 - 5 * a**2 * x**2 - 4 * a * b * x - 8 * b**2 - a**3)
    return tmp
 
def psi_cached(n, tmp, y):
    if n in tmp:
        return tmp[n]
    
    m = n >> 1
    if n & 1:
        psim2 =  psi_cached(m + 2, tmp, y)
        psim1 =  psi_cached(m + 1, tmp, y)
        psim =   psi_cached(m, tmp, y)
        psim_1 = psi_cached(m - 1, tmp, y)
        tmp[n] = psim2 * psim**3 - psim_1 * psim1**3
    else:
        psim2 =  psi_cached(m + 2, tmp, y)
        psim1 =  psi_cached(m + 1, tmp, y)
        psim =   psi_cached(m, tmp, y)
        psim_1 = psi_cached(m - 1, tmp, y)
        psim_2 = psi_cached(m - 2, tmp, y)
    
        tmp[n] = psim * pow(2 * y, -1) * (psim2 * psim_1**2 - psim_2 *psim1**2)
        if len(tmp) % 4000 == 0:
            print(len(tmp))
    
    return tmp[n]

def phi_cached(n, tmp, x, y):
    psin1 =  psi_cached(n+1, tmp, y)
    psin =   psi_cached(n,   tmp, y)
    psin_1 = psi_cached(n-1, tmp, y)
    return x * psin**2 - psin1 * psin_1

def omega_cached(n, tmp, y):
    psin2 =  psi_cached(n + 2, tmp,  y)
    psin1 =  psi_cached(n + 1, tmp, y)
    psin_1 = psi_cached(n - 1, tmp, y)
    psin_2 = psi_cached(n - 2, tmp, y)
    return (psin2 * psin_1**2 - psin_2 * psin1**2) / (4 * y, -1)





# When we do not know y; for example in rings of unknown order

def init_cache_odd(a, b, x):
    tmp = dict()
    tmp[0] = 0
    tmp[1] = 1
    tmp[2] = 2
    tmp[3] = 3 * x**4 + 6 * a * x**2 + 12 * b * x - a**2
    tmp[4] = 4 * (x**6 + 5 * a * x**4 + 20 * b* x**3 - 5 * a**2 * x**2 - 4 * a * b * x - 8 * b**2 - a**3)
    return tmp
 
def psi_odd_cached(n, tmp, y_squared):
    if n in tmp:
        return tmp[n]

    m = n >> 1
    if n & 1:
        psim2 =  psi_odd_cached(m + 2, tmp, y_squared)
        psim1 =  psi_odd_cached(m + 1, tmp, y_squared)
        psim =   psi_odd_cached(m, tmp, y_squared)
        psim_1 = psi_odd_cached(m - 1, tmp, y_squared)

        if m & 1:
            tmp[n] = psim2 * psim**3 - y_squared**2 * psim_1 * psim1**3
        else:
            tmp[n] = y_squared**2 * psim2 * psim**3 - psim_1 * psim1**3

    else:
        psim2 =  psi_odd_cached(m + 2, tmp, y_squared)
        psim1 =  psi_odd_cached(m + 1, tmp, y_squared)
        psim =   psi_odd_cached(m, tmp, y_squared)
        psim_1 = psi_odd_cached(m - 1, tmp, y_squared)
        psim_2 = psi_odd_cached(m - 2, tmp, y_squared)
        
        tmp[n] = psim * (psim2 * psim_1**2 - psim_2 *psim1**2) / 2

        if len(tmp) % 4000 == 0:
            print(len(tmp))
    
    return tmp[n]


if __name__ == "__main__":
    import sys
    from sage.all import Zmod, EllipticCurve, hilbert_class_polynomial, PolynomialRing, factor, randint, GF, var

    pq = 197668727631091367742709136128743654441348626319358455424154957622593478317702875797870917406306610209227069011213796022474557571287640047964204268741387902475941534937803844919846996186015161924763573215768996282673262142495543130448629321245725943457995962053975028414857378181981975537473075371323721723282414965385616238226022585643318380382933957114887587400756839652113664019595783005052456504610440347441432047203456673005694421287910861345275860815765649362917605245331922139276581167277357976312634342038126651764907621538087036263647496919309373580804508215772586118034558441112844163185472846313177715195751594195571775066984403760113841866370735633457655624717485360029766977196336437396823455200244750841891488272955411414597579962144057306870552032004369483951471135636971343453869638618512745435033408701303835819795793685948902753986314730740309492031746077073705183612946948559222867431310158424608457394564821949379990204762408669175695121310052750265910679635011793211354699875527725108376037596187270394487720065110971052499720150365770394956793303385322892341424053711396155971409795818831405230240418721380063162847261865600098988881018781767963959898973351200803986787895261055474025956077155425028344613510741
    
    g = Zmod(pq)
    
    a = g(0)
    b = g(3)
    
    x1 = g(1)
    y1 = g(2)
    e = EllipticCurve(g, [a, b])
    
    n = randint(1, pq-1)
    sys.setrecursionlimit(2 * n.bit_length()) ###########################
    
    cache = init_cache(a, b, x1, y1)
    
    tn = phi_cached(n, cache, x1, y1)
    td = psi_cached(n, cache, y1)**2
    x2 = tn/td
    
    tn = omega_cached(n, cache, y1)
    td = psi_cached(n, cache, y1)**3
    y2 = tn / td
    
    print(e((x2, y2)))
    print(n * e((x1, y1)))
