from math import log, ceil
from oracle import OracleO, OracleC


def get_appr_sessions(n: int, exp: int = 3):
    return exp * ceil(17 * n * log(n))


def recover_kth(key: list[int], n: int, k: int, t: int):
    j = 0
    s = [_ for _ in range(n)]
    for i in range(k):
        j = (j + s[i] + key[i]) % n
        s[j], s[i] = s[i], s[j]

    jx = s.index(t)
    return (jx - j - s[k]) % n


def attack_iv_follows_key(
    n: int, keylen: int, guess: int, main_key: bytes, Oracle=OracleO
):
    key = [guess]

    tfreqs = [dict() for _ in range(keylen)]
    ts = [(0, 0) for _ in range(keylen)]

    for _ in range(get_appr_sessions(n, 3)):  # the number of oracle calls
        o = Oracle(True, main_key=main_key)
        for i in range(1, keylen):  # retrieving the kth byte of prng
            ti = (i - o.call()) % n
            tfreqs[i].setdefault(ti, 0)
            tfreqs[i][ti] += 1

            if (
                tfreqs[i][ti] > ts[i][1]
            ):  # and ti != 2: # getting the most frequent one t
                ts[i] = (ti, tfreqs[i][ti])

    for i in range(1, keylen):
        ki = recover_kth(key, n, i, ts[i][0])
        key.append(ki)

    print(bytes(key))
    print(o.main_key)
    return key


def attack_iv_preceds_key_min_storage(
    n: int, keylen: int, main_key: bytes, Oracle=OracleO
):
    o = Oracle(False, main_key=main_key)
    b = len(o.IV)

    key = []
    for i in range(keylen):
        freqs, km = dict(), (0, 0)
        for _ in range(get_appr_sessions(n, 3)):
            o = Oracle(False, main_key=main_key)
            IV = o.IV

            for _ in range(1, b + i):
                o.call()

            ti = (b + i - o.call()) % n
            ki = recover_kth(list(IV) + key, n, b + i, ti)

            freqs.setdefault(ki, 0)
            freqs[ki] += 1

            if freqs[ki] > km[1]:
                km = (ki, freqs[ki])

        key.append(km[0])
        print(bytes(key))

    print(bytes(key))
    print(o.main_key, o.IV)
    return bytes(key)


def attack_iv_preceds_key_min_time(
    n: int, keylen: int, main_key: bytes, Oracle=OracleO
):
    o = Oracle(False, main_key=main_key)
    b = len(o.IV)

    key = []
    keystreams = []

    print("started oracle calls")
    for _ in range(get_appr_sessions(n, 2)):
        o = Oracle(False, main_key=main_key)
        IV = o.IV
        for _ in range(1, b):
            o.call()

        ts = []
        for i in range(keylen):
            ti = (b + i - o.call()) % n
            ts.append(ti)

        keystreams.append((ts, IV))

    print("started analyzing data")
    for i in range(keylen):
        freqsi, km = dict(), (0, 0)
        for ts, IV in keystreams:
            ki = recover_kth(list(IV) + key, n, b + i, ts[i])

            freqsi.setdefault(ki, 0)
            freqsi[ki] += 1

            if freqsi[ki] > km[1]:
                km = (ki, freqsi[ki])
        key.append(km[0])

    print(bytes(key))
    print(o.main_key)
    return bytes(key)


if __name__ == "__main__":
    main_key = b"flag{of_len_smth_and_smth_flaggy}"

    attack_iv_follows_key(
        n=256,
        keylen=len(main_key),
        guess=main_key[0],
        main_key=main_key,
        Oracle=OracleO,
    )
    print("-" * 50)
    attack_iv_follows_key(
        n=256,
        keylen=len(main_key),
        guess=main_key[0],
        main_key=main_key,
        Oracle=OracleC,
    )
    print("-" * 50)

    attack_iv_preceds_key_min_time(
        n=256, keylen=len(main_key), main_key=main_key, Oracle=OracleO
    )
    print("-" * 50)
    attack_iv_preceds_key_min_time(
        n=256, keylen=len(main_key), main_key=main_key, Oracle=OracleC
    )
    print("-" * 50)
