from math import sqrt

x = 1
for n in range(1, 1000000):
    x = sqrt((1 + 1 / n) ** n * x)
print(x)
x = 1
m = 1
for n in range(1, 100):
    m *= n
    x = x + 1 / m
print(x)

x = 1
for n in range(1, 10000):
    x = (1 + 1 / n) ** n
print(x)
