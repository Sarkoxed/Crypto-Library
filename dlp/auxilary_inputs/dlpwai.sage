
p = 36313

G = GF(p)
g = G.gen()

k = divisors(p-1)
print(k)
#d = k[10]
d = 12104

alpha = randint(1, p-1)
inputs = [pow(g, pow(alpha, i, p-1), p) for i in range(1, d+1)]


