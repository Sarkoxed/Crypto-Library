# лучше для просеивания брать первые sqrt(ln(N)) чисел, для маленьких хватает  2.3.5.7
from math import sqrt, floor


def atkin(a):
    l = []
    for i in range(5, 2 * a):
        l.append(False)

    for x in range(1, floor(sqrt(a)) + 1):
        for y in range(1, floor(sqrt(a)) + 1):
            n = 4 * x**2 + y**2
            if (n < a) and ((n % 12 == 1) or (n % 12 == 5)):
                l[n] = not l[n]
            n -= x**2
            if (n < a) and (n % 12 == 7):
                l[n] = not l[n]
            n -= 2 * y**2
            if (x > y) and (n < a) and (n % 12 == 11):
                l[n] = not l[n]
    for i in range(5, floor(sqrt(a))):
        if l[i]:
            k = i**2
            n = k
            while n <= a:
                l[n] = False
                n += k
    l[2] = True
    l[3] = True

    m = []
    for i in range(len(l)):
        if l[i]:
            m.append(i)
    return m


# atkin(int(input()))
