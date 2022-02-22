def get_pair(a, b):
    r = (a, b)
    z1 = (0, 1)
    z2 = (1, 0)
    while(r[1]):
        d = r[0] // r[1]
        r = (r[1], r[0] - d * r[1])
        z1 = (z1[1], z1[0] - d * z1[1])
        z2 = (z2[1], z2[0] - d * z2[1])
    return (r, z1, z2)

from pprint import pprint

a = int(input())
b = int(input())

pprint(get_pair(a, b))
