import time


def ypattern(n):
    return (6 * n**2 - (-1) ** n * (2 * n + 1) + 6 * n + 1) // 16


def ypattern3(n):
    return (n + 1) * (3 * n + 1) // 8 * (n & 1) + n * (3 * n + 2) // 8 * ((n + 1) & 1)


def ypattern4(n):
    if n & 1:
        return (n + 1) * (3 * n + 1) // 8
    else:
        return n * (3 * n + 2) // 8


# не аналитический способ задания последовательности y в примерно 10 раз медленнее
def ypat2(n):
    l = [1]
    for i in range(1, n + 1):
        if i % 2 != 0:
            l.append(l[i - 1] + (i + 1) // 2)
        else:
            l.append(l[i - 1] + i + 1)
    return l


n = int(input())

x = time.time()
l = [1, 1]

for i in range(n):
    j = 1
    y1 = ypattern(j)
    xk = 0
    while i + 2 - y1 >= 0:
        xk += l[i + 2 - y1] * (-1) ** ((j - 1) // 2)
        y1 = ypattern(j + 1)
        j += 1
    l.append(xk)

z1 = time.time() - x
# print(l, f'последовательность Эйлера - количество разложений числа на сумму {n} ', z1)
print(f"последовательность Эйлера - количество разложений числа на сумму {n} ", z1)


l = [2, 1]

for i in range(n):
    j = 1
    y1 = ypattern(j)
    xk = 0
    while i + 2 - y1 >= 0:
        xk += l[i + 2 - y1] * (-1) ** ((j - 1) // 2)
        y1 = ypattern(j + 1)
        j += 1
    l.append(xk)
    l[0] += 1
# print(l, 'сумма делителей числа n')


"""
l = [1,1]
x = time.time()
for i in range(n):
    j = 1
    y = ypat2(n)
    y1 = y[j-1]
    xk = 0
    while i+2 - y1 >= 0:
        xk += l[i+2 - y1]*(-1)**((j-1)//2)
        y1 = y[j]
        j += 1
    l.append(xk)
z2 = time.time()-x
print(l, f'последовательность Эйлера - количество разложений числа на сумму {n} ', z2)
"""
# print(z2 / z1)

x = time.time()
l = [1, 1]

for i in range(n):
    j = 1
    y1 = ypattern3(j)
    xk = 0
    while i + 2 - y1 >= 0:
        xk += l[i + 2 - y1] * (-1) ** ((j - 1) // 2)
        y1 = ypattern3(j + 1)
        j += 1
    l.append(xk)

z1 = time.time() - x
# print(l, f'последовательность Эйлера - количество разложений числа на сумму {n} ', z1)
print(f"последовательность Эйлера - количество разложений числа на сумму {n} ", z1)

x = time.time()
l = [1, 1]

for i in range(n):
    j = 1
    y1 = ypattern4(j)
    xk = 0
    while i + 2 - y1 >= 0:
        xk += l[i + 2 - y1] * (-1) ** ((j - 1) // 2)
        y1 = ypattern4(j + 1)
        j += 1
    l.append(xk)

z1 = time.time() - x
print(l, f"последовательность Эйлера - количество разложений числа на сумму {n} ", z1)
print(f"последовательность Эйлера - количество разложений числа на сумму {n} ", z1)
