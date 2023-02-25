def gen_knapsack(n, b):
    A = []
    while len(A) != n:
        m = randint(2, b)
        if m not in A:
            A.append(m)
    x = [randint(0, 1) for i in range(n)]
    return A, x, vector(A) * vector(x)

def closest_vertex(M, y):
    ans = M.change_ring(QQ).solve_left(y.change_ring(QQ))
    ans = [round(x) for x in ans]
    return vector(ans) * M

def solve_knapsack(A, s):
    flag = False
    for i in A:
        for j in A:
            if gcd([i, j]) == 1:
                a, b = i, j
                flag = True
                break
        if flag:
            break
 
    m = []
    for i in range(len(A) - 1):
        while True:
            t = [randint(-100, 100) if A[i] not in [a,b] else 0 for i in range(len(A))]
            ss = -vector(t) * vector(A)
            
            s1 = pow(a, -1, b) * ss
            s2 = (pow(b, -1, a) - a) * ss
            assert a * s1 + b * s2 == ss
            p = randint(-100, 100)
            x = s1 - b * p
            y = s2 + a * p
            t[A.index(a)] = x
            t[A.index(b)] = y
            assert vector(t) * vector(A) == 0
            tmp = Matrix(m + [t])
            if tmp.rank() == tmp.dimensions()[0]:
                m.append(t)
                break
        print(Matrix(m).rank())
    
    t = [randint(-100, 100) if A[i] not in [a, b] else 0 for i in range(len(A))]
    ss = -vector(t) * vector(A) + s
    s1 = pow(a, -1, b) * ss
    s2 = (pow(b, -1, a) - a) * ss
    
    p = randint(-100, 100)
    x = s1 - b* p
    y = s2 + a * p
    t[A.index(a)] = x
    t[A.index(b)] = y
    y1 = vector([x - 1/2 for x in t][:-1])
    y = vector([x for x in t][:-1])
    
    m = [x[:-1] for x in m]
    ans = closest_vertex(Matrix(m).LLL(), y1)
    x = ans - y
    return x
