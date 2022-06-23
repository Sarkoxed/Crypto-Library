from Crypto.Util.number import getRandomNBitInteger
from random import randint

def keygen(blocksize: int, nbit=3):
    key = [getRandomNBitInteger(nbit)]
    for i in range(blocksize - 1):
        z = key[-1]
        key.append(randint(2 * z, 2 * z + getRandomNBitInteger(nbit)))
    return key

def encrypt(m: list, key: list):
    s = 0
    for i, j in zip(m, key):
        s += i * j
    return s

def decrypt(s: int, key: list):
    m = list()
    for i in range(len(key)-1, -1, -1):
        if(s >= key[i]):
            m = [1] + m
            s -= key[i]
        else:
            m = [0] + m
    if(s != 0):
        raise "pidoras"
    return m

if __name__ == "__main__":
    print(1)

