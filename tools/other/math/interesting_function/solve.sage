def get_integ(n, a=0, b=1):
    d = get_f(n)
    d = sorted(list(d.items()), key=lambda x: x[0])
    su = 0
    for i in range(len(d) - 1):
        if d[i][0] < a:
            continue
        elif d[i][0] > b:
            continue
        x0, y0 = d[i]
        x1, y1 = d[i + 1]
        fl = x1 - x0
        fu = (y0 + y1) / 2
        su += fu * fl
    return su


def get_f(n):
    d = dict()
    d[1/2] = 1
    d[0] = 0
    for i in range(2, n):
        for j in range(0, 2**(i - 1), 2):
            d[2**(-i) + (j) * 2**(-i)] = 1 / (1/(d[2**(-i + 1) + (j) * 2**(-i + 1)])+ 1)
            d[1 - 2**(-i) - (j) * 2**(-i)] = (1/(d[2**(-i + 1) + (j) * 2**(-i + 1)])+ 1)
    return d


print(get_integ(19).n())
