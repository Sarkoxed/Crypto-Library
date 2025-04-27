# https://www.youtube.com/watch?v=Z9fODwmed6M&list=PLTOTGx3fVhMSW5D0BOtL5dVGYwCVlyhfd&index=72
# https://en.wikipedia.org/wiki/Non-uniform_random_variate_generation

# TODO: F_X(X) -> U -> G_Y^-1(U) -> Y(G_Y(y) - cdf of Y)
# TODO: discrete too

import numpy as np
from numpy import sqrt
from scipy.special import erf, erfinv  # can be directly applied to np vectors btw

from hist_plotter import hist_plot

n = 100_000
uniform = np.random.random(size=n)
hist_plot(uniform)
normal = np.random.normal(size=n)
hist_plot(normal)


def inverse_normal(x):
    return 1 / 2 * (1 + erf(x / sqrt(2)))


tu = np.vectorize(inverse_normal)(normal)
hist_plot(tu)


def normal(x):
    return sqrt(2) * erfinv(2 * x - 1)


tn = np.vectorize(normal)(uniform)
hist_plot(tn)
