from math import log, ceil
from oracle import OracleO as Oracle

# from oracle import OracleC as Oracle


def get_appr_sessions(n: int):
    return 3 * ceil(18 * n * log(n))


def recover_kth(key: list[int], n: int, k: int, t: int):
    j = 0
    s = [_ for _ in range(n)]
    for i in range(k):
        j = (j + s[i] + key[i]) % n
        s[j], s[i] = s[i], s[j]

    jx = s.index(t)
    return (jx - j - s[k]) % n


def get_s_1(key: list[int], n: int):
    j = 0
    s = [_ for _ in range(n)]
    for i in range(len(key)):
        j = (j + s[i] + key[i]) % n
        s[j], s[i] = s[i], s[j]
    return s[1]


def attack_iv_preceds_key(n: int, keylen: int):
    o = Oracle(False)
    b = len(o.IV)

    key = []

    tfreqs = [dict() for _ in range(keylen)]
    ts = [(0, 0, []) for _ in range(keylen)]

    for _ in range(get_appr_sessions(n)):
        print(_)
        o = Oracle(False)
        IV = o.IV

        for i in range(n):
            o.call()

        for i in range(keylen):
            if get_s_1(IV, n) == b + i:
                ti = (i + 1 - o.call()) % n
                tfreqs[i].setdefault(ti, 0)
                tfreqs[i][ti] += 1

                if tfreqs[i][ti] > ts[i][1]:
                    ts[i] = (ti, tfreqs[i][ti], list(IV))

    for i in range(keylen):
        ki = recover_kth(ts[i][2] + key, n, b + i, ts[i][0])
        key.append(ki)

    print(key, bytes(key))


attack_iv_preceds_key(256, 4)
