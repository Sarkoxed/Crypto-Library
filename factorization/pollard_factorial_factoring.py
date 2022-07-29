from sage.all import *
from time import time, sleep
from pylab import plot, show


def PollardP(n, z):
    while True:
        a = randint(2, n)
        for i in range(1, pow(2, z)):
            a = pow(a, i, n)
            if a - 1 == 0:
                break
            if gcd(a - 1, n) == 1:
                continue
            print(a, i)
            return gcd(a - 1, n)


def time_check(nbit, n):
    m = 0
    for i in range(n):
        z1, z2 = random_prime(2**nbit), random_prime(2**nbit)
        k = z1 * z2
        print(f"--------------{i+1} test-------------")
        print(f"p = {z1}, q = {z2}, p*q = {k}")
        x = time()
        PollardP(k)
        x = time() - x
        m += x
        print(f"time: {x}")
        print(f"-------------------------------------")
    print(f"nbit: {nbit},average time: {m / n}")
    return m / n


if __name__ == "__main__":
    n = int(input("factor what? "))
    nbits = int(input("how many bits to factorial? "))
    print(PollardP(n, nbits))
#    t = []
#    for i in range(15):
#        t.append(time_check(20 + i, 10))
#        print("5 sec to think")
#        sleep(5)
#    x = plot(range(20, 35), t)
#    show()
