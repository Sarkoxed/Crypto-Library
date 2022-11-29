from math import log, ceil
from oracle import OracleO as Oracle

# from oracle import OracleC as Oracle


def get_appr_sessions(n: int):
    return 3 * ceil(17 * n * log(n))


def recover_kth(key: list[int], n: int, k: int, t: int):
    j = 0
    s = [_ for _ in range(n)]
    for i in range(k):
        j = (j + s[i] + key[i]) % n
        s[j], s[i] = s[i], s[j]

    jx = s.index(t)
    return (jx - j - s[k]) % n


def attack_iv_follows_key(n: int, keylen: int, guess: int):
    key = [guess]

    tfreqs = [dict() for _ in range(keylen)]
    ts = [(0, 0) for _ in range(keylen)]

    for _ in range(get_appr_sessions(n)):  # the number of oracle calls
        o = Oracle(True)
        for i in range(1, keylen):  # retrieving the kth byte of prng
            ti = (i - o.call()) % n
            tfreqs[i].setdefault(ti, 0)
            tfreqs[i][ti] += 1

            if tfreqs[i][ti] > ts[i][1] and ti != 2:
                ts[i] = (ti, tfreqs[i][ti])

    for i in range(1, keylen):
        ki = recover_kth(key, n, i, ts[i][0])
        key.append(ki)

    print(key, ts, bytes(key))


def attack_iv_preceds_key(n: int, keylen: int):
    o = Oracle(False)
    b = len(o.IV)

    key = []

    tfreqs = [dict() for _ in range(keylen)]
    ts = [(0, 0, []) for _ in range(keylen)]

    for _ in range(get_appr_sessions(n)):
        o = Oracle(False)
        IV = o.IV

        for i in range(1, b):
            o.call()

        for i in range(keylen):
            ti = (b + i - o.call()) % n
            tfreqs[i].setdefault(ti, 0)
            tfreqs[i][ti] += 1

            if tfreqs[i][ti] > ts[i][1]:
                ts[i] = (ti, tfreqs[i][ti], list(IV))

    for i in range(keylen):
        ki = recover_kth(ts[i][2] + key, n, b + i, ts[i][0])
        key.append(ki)

    print(key, ts[:10], bytes(key), len(key))


#attack_iv_follows_key(n=256, keylen=28, guess=ord('O'))
attack_iv_preceds_key(n=256, keylen=14)
