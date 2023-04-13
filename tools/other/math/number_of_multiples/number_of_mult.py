# This program multiplies all the digits of a number until it becomes a single digit
def per(n):
    j = 0
    while n > 10:
        k = 1
        for i in str(n):
            k *= int(i)
        n = k
        j += 1
    return j


max = 0
for i in range(100000000):
    k = per(i)
    if k > max:
        print(f"STEPS : {k}, NUMBER : {i}")
        max = k
