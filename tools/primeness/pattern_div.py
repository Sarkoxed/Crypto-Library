def euler(n):
    # n = int(input())
    l = [2, 1]
    k = []
    for i in range(n):
        j = 1
        y1 = 1  # первое число последовательтности у
        xk = 0

        while i + 2 - y1 >= 0:
            xk += l[i + 2 - y1] * (-1) ** ((j - 1) // 2)

            if (j + 1) & 1:
                y1 = (j + 2) * (3 * j + 4) // 8
            else:
                y1 = (j + 1) * (3 * j + 5) // 8

            j += 1

        l.append(xk)
        if l[-1] == (len(l)):
            k.append(len(l) - 1)
        l[0] += 1
    return k
