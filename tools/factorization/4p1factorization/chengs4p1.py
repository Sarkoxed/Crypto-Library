import random
from Crypto.Util.number import isPrime
from sage.all import Zmod, EllipticCure

def get_complex_prime():
    D = 427
    while True:
        s = random.randint(2 ** 1020, 2 ** 1021 - 1)
        tmp = D * s ** 2 + 1
        if tmp % 4 == 0 and isPrime((tmp // 4)):
            return tmp // 4


def 
