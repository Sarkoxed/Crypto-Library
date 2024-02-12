from sage.all import GF, EllipticCurve, is_prime, randint


def rebase(n, b):
    if n < b:
        return [n]
    else:
        return [n % b] + rebase(n // b, b)


# q(x, y) = (x^q, y^q) + (x^(q^2), -y^(q^2))
def mul_anom(P, k, q):
    e = P.curve()
    based = rebase(k, q)

    points_map = dict()
    res = P * 0

    for i, ki in enumerate(based):
        Pi, power = points_map.setdefault(ki, (P * ki, 0))
        pix, piy = Pi.xy()

        for j in range(i - power):
            pixq = pix**q
            piyq = piy**q
            newPi = e((pixq, piyq)) + e((pixq**q, -(piyq**q)))
            pix, piy = newPi.xy()

        Piqi = e((pix, piy))
        points_map[ki] = (Piqi, i)
        res += Piqi
    return res
