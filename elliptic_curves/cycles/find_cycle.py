from sage.all import EllipticCurve, GF, random_prime

from tqdm import tqdm
import itertools as it

n = 128
B = 20
while True:
    p = random_prime(2**n)
    G = GF(p)
    for a, b in tqdm(it.product(range(-B, B + 1), repeat=2), total=(2 * B + 1)**2):
        try:
            e = EllipticCurve(G, [a, b])
        except:
            continue
        q = e.order()
        if q.is_prime():
            break

    G = GF(q)
    for c, d in tqdm(it.product(range(-B, B + 1), repeat=2), total=(2 * B + 1)**2):
        try:
            e = EllipticCurve(G, [c, d])
        except:
            continue
        r = e.order()
        if r == p:
            break
    else:
        continue
    break

print(f"E: {p, a, b}")
print(f"E: {q, c, d}")
