from math import sqrt, floor

def sundaram(n):
    l = []
    for i in range(1, 2*n):
        l.append(True)
    for i in range(1, floor((sqrt(2*n+1)-1)/2)+1):
        for j in range(i, floor((n-i)/(2*i+1))+1):
            l[i*j*2+i+j] = False
    r = []
    for i in range(n+1):
        if l[i]:
            r.append(2*i+1)
    return r
    #print(r)

#Sundaram(int(input()))
