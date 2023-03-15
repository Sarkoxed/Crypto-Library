def get_pair(a, b):
    r = (a, b)
    z1 = (0, 1)
    z2 = (1, 0)
    while r[1]:
        d = r[0] // r[1]
        r = (r[1], r[0] - d * r[1])
        z1 = (z1[1], z1[0] - d * z1[1])
        z2 = (z2[1], z2[0] - d * z2[1])
    return (r, z1, z2)

def prod_m(l, p):
    ans = 1
    for x in l:
        ans = (ans * x) % p
    return ans

def montgomery(l, p):
    a = prod_m(l, p)
    a_i = pow(a, -1, p)
    res = [(prod_m(l[:i] + l[i + 1:], p) * a_i) % p for i in range(len(l))]
    return res

if __name__ == "__main__":
    #from pprint import pprint
    #
    #a = int(input())
    #b = int(input())
    #
    #pprint(get_pair(a, b))

    from time import time
    from Crypto.Util.number import getPrime
    from random import randint
    
    p = getPrime(1024)
    n = 1000
    l = [randint(0, p-1) for _ in range(n)]
    
    start = time()
    m = [pow(x, p-2, p) for x in l]
    end = time()
    print(f"pow(x, p-2, p): {end - start}")
    
    start = time()
    m1 = [pow(x, -1, p) for x in l]
    end = time()
    print(f"pow(x, -1, p): {end - start}")
 
    start = time()
    m2 = montgomery(l, p)
    end = time()
    print(f"mont: {end - start}")

    assert m1 == m2 and m1 == m
