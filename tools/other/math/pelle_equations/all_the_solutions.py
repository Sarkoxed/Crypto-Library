from sage.all import *


def getBasis(a, b, d, c):
    z_bound = (a + b * sqrt(d) + abs(c)) / 2
    t_bound = (a + b * sqrt(d) + abs(c)) / (2 * sqrt(d))
    ans = []
    if z_bound > t_bound:
        for i in range(-ceil(t_bound), ceil(t_bound)):
            a1 = sqrt(c + i**2 * d)
            a2 = -1 * a1
            if a1.is_integer():
                if 1 < a1 + i * sqrt(d) <= a + b * sqrt(d):
                    ans.append((a1, i))
                if 1 < a2 + i * sqrt(d) <= a + b * sqrt(d):
                    ans.append((a2, i))
        return ans
    else:
        for i in range(-ceil(z_bound), ceil(z_bound)):
            a1 = sqrt(i**2 - c) / d
            a2 = -1 * a1
            if a1.is_integer():
                if 1 < i + a1 * sqrt(d) <= a + b * sqrt(d):
                    ans.append((i, a1))
                if 1 < i + a2 * sqrt(d) <= a + b * sqrt(d):
                    ans.append((i, a2))
        return ans


def naive_search_trivia_sol(d: int, n: int = 10000):
    for i in range(2, n):
        if sqrt((i**2 - 1) / d).is_integer():
            return (i, sqrt((i**2 - 1) / d))


def cycle_method(d):
    r0 = floor(sqrt(d))
    r1 = ceil(sqrt(d))
    if abs(r0**2 - d) > abs(r1**2 - d):
        x, y = r1, 1
    else:
        x, y = r0, 1

    while True:
        if x**2 - d * y**2 == 1:
            return (x, y)

        a0 = abs(x**2 - d * y**2)
        r = int((-x * pow(y, -1, a0)) % a0)

        n1, n2 = floor((sqrt(d) - r) / a0), ceil((sqrt(d) - r) / a0)
        if abs((r + n1 * a0) ** 2 - d) > abs((r + n2 * a0) ** 2 - d):
            r1 = r + n2 * a0
        else:
            r1 = r + n1 * a0

        r = r1
        x, y = r * x + d * y, y * r + x
        s = r**2 - d
        assert x % a0 == 0
        assert y % a0 == 0
        assert s * a0 % (a0**2) == 0
        x //= a0
        y //= a0


def england_method(d):
    r0 = floor(sqrt(d))
    r1 = ceil(sqrt(d))
    if abs(r0**2 - d) > abs(r1**2 - d):
        x, y = r1, 1
    else:
        x, y = r0, 1

    while True:
        if x**2 - d * y**2 == 1:
            return (x, y)

        a0 = abs(x**2 - d * y**2)
        r = int((-x * pow(y, -1, a0)) % a0)

        n1, n2 = floor((sqrt(d) - r) / a0), ceil((sqrt(d) - r) / a0)

        r = r + n1 * a0
        x, y = r * x + d * y, y * r + x
        s = r**2 - d
        assert x % a0 == 0
        assert y % a0 == 0
        assert s * a0 % (a0**2) == 0
        x //= a0
        y //= a0


if __name__ == "__main__":
    #c, d = int(input()), int(input())
    # q = naive_search_trivia_sol(d)
    #q = cycle_method(d)
    #print(q)
    #for i in range(2, 150):
    #    if not sqrt(i).is_integer():
    #        print(england_method(i), i)
    c, d = 11035088936239727592975273948400856248132189366824211207031291894071035986791900612814999508457245777184300286664488882627219844048061616295329549707634025659232733878253368773852677080071321116069150420136491859869284439529481891838729531010563421129564975265412715621313004370783536088787661725454330361772613878175997577412503328803799693865065526765849670407210062389629694697856444218860199941097641302890357172736824200822308560708434579060126444810830945, 111578009802636409437123757591617048189760145423552421418627338749835916561801
    q = england_method(d)
    print(q)
    #r = getBasis(*q, d, c)
    #print(r)
