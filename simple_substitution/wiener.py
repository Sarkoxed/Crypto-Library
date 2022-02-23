from string import ascii_lowercase, ascii_uppercase, punctuation, digits
from sys import argv
import json


ext = punctuation + digits

cip_t = dict()
for i in range(len(ascii_lowercase)):
    cip_t[ascii_lowercase[i]] = dict(zip(ascii_lowercase, ascii_lowercase[i:] + ascii_lowercase[:i]))

def encrypt(s: str, k: str):
    x = len(s) // len(k)
    k *= (x + 1)
    return "".join(cip_t[k[i]][s[i]] for i in range(len(s)))

def decrypt(s: str, k: str):
    x = len(s) // len(k)
    k *= (x + 1)
    ans = []
    for i in range(len(s)):
        ans.append(list(cip_t['a'].values())[list(cip_t[k[i]].values()).index(s[i])])
    return "".join(ans)

#def brute(s: str):
#    #guessing the length of the key
#    for n in range(1, len(s)):



def main():
    if(len(argv) == 1):
        print("--help for help")
    elif(argv[1] == "help"):
        print("enc <plain> <key>")
        print("dec <cip> <key>")
        print("brute <cip>")
        print("freq <cip>")
        print("brfreq <cip>")
    elif(argv[1] == "enc"):
        print(encrypt(argv[2], argv[3]))
    elif(argv[1] == "dec"):
        print(decrypt(argv[2], argv[3]))
#    elif(argv[1] == "brute"):
#        brute(argv[2])
#    elif(argv[1] == "freq"):
#        freq(argv[2])
#    elif(argv[1] == "brfreq"):
#        brfreq(argv[2])

if __name__ == '__main__':
    main()


