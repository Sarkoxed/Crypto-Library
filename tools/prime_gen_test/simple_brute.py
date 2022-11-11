from math import sqrt, floor


def prime(N):
    flag = False
    for i in range(11, floor(sqrt(N)) + 1, 2):
        flag = N % i == 0
        if flag:
            break
    return not flag


def simp(n):  # можно в принципе уже начинать с к = 1 но пока для проверки вот так
    l = [
        1,
        11,
        13,
        17,
        19,
        23,
        29,
        31,
        37,
        41,
        43,
        47,
        53,
        59,
        61,
        67,
        71,
        73,
        79,
        83,
        89,
        97,
        101,
        103,
        107,
        109,
        113,
        127,
        131,
        137,
        139,
        149,
        151,
        157,
        163,
        167,
        173,
        179,
        181,
        191,
        193,
        197,
        199,
    ]
    r = [2, 3, 5, 7]
    k = 0
    while (210 * k + 1) < n:
        for i in range(len(l)):
            t = 210 * k + l[i]
            if prime(t):
                r.append(t)
        k += 1
    # print(r)


simp(int(input()))
