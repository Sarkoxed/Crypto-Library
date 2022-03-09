from string import ascii_lowercase, ascii_uppercase, punctuation, digits
from sys import argv
import json

ext = punctuation + digits

def encrypt(s: str, n: int):
    s = s.lower()
    d = dict(zip(ascii_lowercase + ext, ascii_lowercase[1:] + ascii_lowercase[:1] + ext))
    return "".join(d[x] for x in s)


def decrypt(s: str, n: int):
    s = s.lower()
    d = dict(zip(ascii_lowercase[1:] + ascii_lowercase[:1] + ext, ascii_lowercase + ext))
    return "".join(d[x] for x in s)

def brute(s: str):
    s = s.lower()
    for i in range(26):
        a = ascii_lowercase[i:] + ascii_lowercase[:i]
        d = dict(zip(a + ext, ascii_lowercase + ext))
        print("".join([d[x] for x in s]))

def freq(s: str):
    s1 = json.loads(open("frequencies/one.json", "r").read())
    s2 = json.loads(open("frequencies/bi.json", "r").read())
    s = s.lower()

    if(len(s) == 0):
        return

    d1 = dict()
    for _ in s:
        d1.setdefault(_, 0)
        d1[_] += 1

    for i, j in d1.items():
        d1[i] = j / len(s)

#    ----------------------------------------


def main():
    if(len(argv) == 1):
        print("--help for help")
    elif(argv[1] == "help"):
        print("enc <plain> <rot>")
        print("dec <cip> <rot>")
        print("brute <cip>")
        print("freq <cip>")
        print("brfreq <cip>")
    elif(argv[1] == "enc"):
        encrypt(argv[2], int(argv[3]))
    elif(argv[1] == "dec"):
        decrypt(argv[2], int(argv[3]))
    elif(argv[1] == "brute"):
        brute(argv[2])
#    elif(argv[1] == "freq"):
#        freq(argv[2])
#    elif(argv[1] == "brfreq"):
#        brfreq(argv[2])

if __name__ == '__main__':
    main()

