import matplotlib.pyplot as plt
from numpy import arange, sin, pi, cos
from math import gcd


def print_pattern(n0, nk, name, pattern):
    t = arange(n0, nk, 1)  # создаём список от 2.0 до 2.0 с шагом 0.01
    # plt.axis([0, 1000, 0, 1000]) #«обрезаем» картинку от -1 до 2 по OX и от -1 до 1 по OY
    plt.title(name)
    fig, ax = plt.subplots()
    ax.plot(t, pattern)


def flyitgoddamit(n):
    l = [1, 1]
    for i in range(2, n):
        if gcd(i, l[i - 1]) == 1:
            l.append(l[i - 1] + i + 1)
        else:
            l.append(l[i - 1] // gcd(i, l[i - 1]))
    return l


print_pattern(0, 1000, "fly", flyitgoddamit(1000))
