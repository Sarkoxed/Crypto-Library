def ternary_n(x, a, b, e=1 / 2):
    c, d = a + (b - a) / 3, a + (b - a) * 2 / 3
    if x <= d and x >= c:
        return e
    elif x < c:
        return ternary_n(x, a, c, e - 1 / (e.denominator() * 2))
    elif x > d:
        return ternary_n(x, d, b, e + 1 / (e.denominator() * 2))


p1 = plot(lambda x: ternary_n(x, 0, 1), 0, 1)
p1.show()
