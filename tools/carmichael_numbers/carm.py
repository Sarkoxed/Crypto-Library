from sage.all import is_prime


def get_carm_dumb(nbit):
    t = 2**nbit
    s = 0
    while True:
        # print(s)

        k = t + s
        a = 6 * k + 1
        if not is_prime(a):
            s += 1
            continue
        b = 12 * k + 1
        if not is_prime(b):
            s += 1
            continue
        c = 18 * k + 1
        if is_prime(c):
            return a, b, c
        s += 1
