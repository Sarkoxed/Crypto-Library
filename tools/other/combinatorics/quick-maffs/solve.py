from itertools import permutations
from sage.all import binomial

def get_n(n):
     ass = [1, 1]
     for i in range(2, n + 1):
         ass.append(sum(binomial(i-1, j) * ass[j] * ass[i - 1 - j] for j in range(i)) // 2)
     return ass[-1]

def get_brute(n):
    c = 0
    for x in permutations(range(1, n + 1)):
        if all((x[i-1] < x[i] and i % 2 == 1) or ((x[i-1] > x[i]) and i % 2 == 0) for i in range(1, n)):
            c += 1
            print(x)

    print(f"{c = }")
    return c

get_brute(5)
#print(get_n(11))
#print(get_brute(11))
for n in range(2, 40):
    print(get_n(n) % (10**9 + 7))
