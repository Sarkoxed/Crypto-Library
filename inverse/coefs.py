def coefs(a, b):
    u, g, x, y = 1, a, 0, b
    while(1):
        if(y == 0):
            v = (g - a * u) // b
            return (g, u ,v)
        s = u - (g // y) * x
        u,g,x,y = x, y, s, g % y


print(coefs(17, 21))
