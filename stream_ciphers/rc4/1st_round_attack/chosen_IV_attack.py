from math import ceil, log
from os import urandom

from oracle import OracleC, OracleO


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


def get_s(key: list[int], n: int):
    j = 0
    s = [_ for _ in range(n)]
    for i in range(len(key)):
        j = (j + s[i] + key[i]) % n
        s[j], s[i] = s[i], s[j]
    return s, j


def get_iv(ivlen: int, ned: int):
    while True:
        iv = bytes([0, ned - 1]) + urandom(ivlen - 2)
        s, j = get_s(list(iv), 256)
        if s[1] == ned:
            return iv


def chosen_IV_attack_onto_first_byte(
    n: int, keylen: int, main_key: bytes, IVsfile: str, Oracle=OracleO
):
    b = 256 - keylen

    key = []
    print("Started oracle calls")
    for c in range(keylen):
        t = b + c
        print(t)
        freqs, k = dict(), (0, 0)
        for _ in range(100):
            IV = get_iv(b, t)
            IV = bytes(IV)

            o = Oracle(False, main_key=main_key, IV=IV)
            x = o.call()

            s, j = get_s(list(IV) + key, n)
            if s[1] != t:
                continue

            T = {j: i for i, j in enumerate(s)}
            ki = (T[(T[x] - t) % n] - j - s[t]) % n

            freqs.setdefault(ki, 0)
            freqs[ki] += 1
            if freqs[ki] > k[1]:
                k = (ki, freqs[ki])

        key.append(k[0])
        print(bytes(key))

    print(bytes(key))
    print(o.main_key)

    return bytes(key)


if __name__ == "__main__":
    key = b"flag{of_length_smth_and_smth_flaggy}"[:34]
    b = 256 - len(key)
    IVsfile = f"../special_ivs/db/IV_{b}.json"
    chosen_IV_attack_onto_first_byte(
        n=256, keylen=len(key), main_key=key, IVsfile=IVsfile, Oracle=OracleO
    )
