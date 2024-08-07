from division_polynomial import (
    init_cache,
    phi_cached,
    psi_cached,
    omega_cached,
    init_cache_noy,
    phi_cached_noy,
    psi_cached_noy,
    omega_cached_noy,
)
from sage.all import Zmod, GF, random_prime, EllipticCurve, legendre_symbol, crt
from random import randint
import pytest


def gen_params():
    p = random_prime(2**254)
    g = GF(p)
    a = g.random_element()
    b = g.random_element()
    e = EllipticCurve(g, [a, b])
    r = e.random_element()
    n = randint(0, p)
    return p, g, a, b, e, r, n


@pytest.mark.parametrize("p, g, a, b, e, r, n", [gen_params()])
def test_cached(p, g, a, b, e, r, n):
    x, y = r.xy()

    cache = init_cache(a, b, x, y)
    phi = phi_cached(n, cache, x, y)
    psi = psi_cached(n, cache, y)
    omega = omega_cached(n, cache, y)

    x1 = phi / psi**2
    y1 = omega / psi**3

    assert e((x1, y1)) == n * r


@pytest.mark.parametrize("p, g, a, b, e, r, n", [gen_params()])
def test_cached_noy(p, g, a, b, e, r, n):
    x = r[0]
    y_squared = x**3 + a * x + b

    cache = init_cache_noy(a, b, x)
    phi = phi_cached_noy(n, cache, x, y_squared)
    psi = psi_cached_noy(n, cache, y_squared)
    omega = omega_cached_noy(n, cache, y_squared)

    x1 = phi / psi**2
    y1 = omega / psi**3

    y = r[1]
    if n % 2 == 0:
        x1 /= x**3 + a * x + b
        y1 /= (x**3 + a * x + b) * y
    else:
        y1 *= y
    assert e((x1, y1)) == n * r


pq = 197668727631091367742709136128743654441348626319358455424154957622593478317702875797870917406306610209227069011213796022474557571287640047964204268741387902475941534937803844919846996186015161924763573215768996282673262142495543130448629321245725943457995962053975028414857378181981975537473075371323721723282414965385616238226022585643318380382933957114887587400756839652113664019595783005052456504610440347441432047203456673005694421287910861345275860815765649362917605245331922139276581167277357976312634342038126651764907621538087036263647496919309373580804508215772586118034558441112844163185472846313177715195751594195571775066984403760113841866370735633457655624717485360029766977196336437396823455200244750841891488272955411414597579962144057306870552032004369483951471135636971343453869638618512745435033408701303835819795793685948902753986314730740309492031746077073705183612946948559222867431310158424608457394564821949379990204762408669175695121310052750265910679635011793211354699875527725108376037596187270394487720065110971052499720150365770394956793303385322892341424053711396155971409795818831405230240418721380063162847261865600098988881018781767963959898973351200803986787895261055474025956077155425028344613510741


@pytest.mark.parametrize("pq, n", [(pq, randint(1, pq - 1))])
def test_zmod(pq, n):
    import sys

    g = Zmod(pq)

    a = g(0)
    b = g(3)

    x1 = g(1)
    y1 = g(2)
    e = EllipticCurve(g, [a, b])

    sys.setrecursionlimit(2 * n.bit_length())  ###########################

    cache = init_cache(a, b, x1, y1)

    tn = phi_cached(n, cache, x1, y1)
    td = psi_cached(n, cache, y1) ** 2
    x2 = tn / td

    tn = omega_cached(n, cache, y1)
    td = psi_cached(n, cache, y1) ** 3
    y2 = tn / td

    assert e((x2, y2)) == n * e((x1, y1))


def get_zmod_params():
    p = random_prime(2**100)
    q = random_prime(2**100)

    g = Zmod(p * q)
    gp = GF(p)
    gq = GF(q)
    a = g.random_element()
    b = g.random_element()

    while True:
        x = g.random_element()
        y_squared = x**3 + a * x + b
        if legendre_symbol(y_squared, p) != 1 or legendre_symbol(y_squared, q) != 1:
            continue

        y_p = gp(y_squared).sqrt()
        y_q = gq(y_squared).sqrt()

        y = crt([int(y_p), int(y_q)], [p, q])
        break

    n = randint(1, p * q - 1)
    return g, p, q, a, b, x, y, n


@pytest.mark.parametrize("g, p, q, a, b, x, y, n", [get_zmod_params()])
def test_cached_noy_zmod(g, p, q, a, b, x, y, n):
    e = EllipticCurve(g, [a, b])
    r = e((x, y))

    y_squared = x**3 + a * x + b

    cache = init_cache_noy(a, b, x)
    phi = phi_cached_noy(n, cache, x, y_squared)
    psi = psi_cached_noy(n, cache, y_squared)
    omega = omega_cached_noy(n, cache, y_squared)

    x1 = phi / psi**2
    y1 = omega / psi**3

    if n % 2 == 0:
        x1 /= x**3 + a * x + b
        y1 /= (x**3 + a * x + b) * y
    else:
        y1 *= y
    assert e((x1, y1)) == n * r
