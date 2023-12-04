from string import ascii_lowercase, ascii_uppercase, punctuation, digits
from sys import argv
import json

# ext = punctuation + digits
# alph = ascii_lowercase
alph = ascii_lowercase + digits
ext = punctuation


def encrypt(s: str, n: int):
    s = s.lower()
    d = dict(zip(alph + ext, alph[n:] + alph[:n] + ext))
    return "".join(d[x] for x in s)


def decrypt(s: str, n: int):
    s = s.lower()
    d = dict(zip(alph[n:] + alph[:n] + ext, alph + ext))
    return "".join(d[x] for x in s)


def brute(s: str):
    s = s.lower()
    for i in range(26):
        a = alph[i:] + alph[:i]
        d = dict(zip(a + ext, alph + ext))
        print("".join([d[x] for x in s]))


def freq(s: str):
    s1 = json.loads(open("frequencies/one.json", "r").read())
    s2 = json.loads(open("frequencies/bi.json", "r").read())
    s = s.lower()

    if len(s) == 0:
        return

    d1 = dict()
    for _ in s:
        d1.setdefault(_, 0)
        d1[_] += 1

    for i, j in d1.items():
        d1[i] = j / len(s)


if __name__ == "__main__":
    main()
