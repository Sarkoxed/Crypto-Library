from functools import partial
from random import getrandbits, randint

import numpy as np
from hist_plotter import hist_plot


def random(nbit: int, lsb=False):
    r = getrandbits(nbit)
    ms = randint(0, nbit)

    if lsb:
        return r & ((1 << ms) - 1)
    return r >> ms


def random1(nbit):
    r = getrandbits(randint(0, nbit))
    return r


N = 10
M = 100_000

data1 = np.array([random(N, True) for _ in range(M)])
data2 = np.array([random(N, False) for _ in range(M)])
data3 = np.array([random1(N) for _ in range(M)])

hist_plot(data1)#, "LSB")
hist_plot(data2)#, "MSB")
hist_plot(data2)#, "FRF")

print(list(data1).count(0))
print(list(data2).count(0))
print(list(data3).count(0))
print(list(data1).count(512))
print(list(data2).count(512))
print(list(data3).count(512))
