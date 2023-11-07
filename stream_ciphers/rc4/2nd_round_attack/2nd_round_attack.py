from math import log, ceil
from oracle import OracleO, OracleC


def get_appr_sessions(n: int, exp: int = 3):
    return exp * ceil(18 * n * log(n))


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


def attack_iv_preceds_key(n: int, keylen: int, main_key: bytes, Oracle=OracleO):
    o = Oracle(False, main_key=main_key)
    b = len(o.IV)

    key = []

    keystreams = []

    sessions = n * get_appr_sessions(n, 1)
    for _ in range(sessions):
        o = Oracle(False)
        IV = o.IV

        for i in range(n):
            o.call()

        ts = []
        for i in range(keylen):
            if get_s_1(IV, n) == b + i:
                ti = (i + 1 - o.call()) % n
                ts.append(ti)

        keystreams.append((ts, IV))

    for i in range(keylen):
        freqsi, km = dict(), (0, 0)
        for ts, IV in keystreams:
            if get_s_1(IV, n) == b + i:

                ki = recover_kth(list(IV) + key, b + i, ts[i])
                freqsi.setdefault(ki, 0)
                freqsi[ki] += 1

                if freqsi[ki] > km[1]:
                    km = (ki, freqsi[ki])
        km.append(km[0])

    print(o.main_key, bytes(key))
    return bytes(key)


if __name__ == "__main__":
    main_key = b"flag{of_len_smth_and_smth_flaggy}"
    attack_iv_preceds_key(
        n=256, keylen=len(main_key), main_key=main_key, Oracle=OracleO
    )
