from sage.all import gcd, log, vector, Matrix, sqrt, identity_matrix, randint, floor, ceil

def gen_a(n, A):
    ass = []
    while len(ass) < n:
        a = randint(1, A)
        if all(gcd(a, r) == 1  for r in ass):
            ass.append(a)
    return ass

A = 10**10
n = 5
ass = gen_a(n, A)
d = n / max((log(x) / log(2)).n() for x in ass)
assert d.n() < 2 / n

def nearest(x):
    if abs(x - floor(x)) < 0.5:
        return floor(x)
    return ceil(x)

def find_random_solution(ass, B):
    assert all(gcd(a, b) == 1 or a == b for a in ass for b in ass)
    rand_sol = [randint(-B, B) for _ in range(len(ass) - 2)]
    while gcd(sum(a * b for a, b in zip(rand_sol, ass)), ass[-2]) != 1:
        rand_sol = [randint(-B, B) for _ in range(len(ass) - 2)]
    res_sum = sum(a * b for a, b in zip(rand_sol, ass))
    if res_sum < 0:
        rand_sol = [-x for x in rand_sol]
        res_sum = - res_sum

    c1 = pow(res_sum, -1, ass[-2])
    c2 = pow(ass[-2], -1, res_sum) - res_sum
    assert c1 * res_sum + c2 * ass[-2] == 1
    rand_sol = [x * c1 * ass[-1] for x in rand_sol]
    rand_sol.append(c2 * ass[-1])
    rand_sol.append(-1)
    assert sum(a * b for a, b in zip(rand_sol, ass)) == 0
    return rand_sol

print(find_random_solution(ass, 10))
exit()

M = Matrix(len(ass), len(ass) + 1)
M.set_block(0, 0, identity_matrix(len(ass)))
M.set_block(0, len(ass), Matrix(ass).T)

def gram_det(M):
    A = Matrix(M.nrows())
    for i in range(M.nrows()):
        for j in range(M.nrows()):
            A[i, j] = M[i] * M[j]
    return sqrt(abs(A.det()))

def gram_det2(M):
    return sqrt((M * M.T).det())

def babai_closest_plain(t, basis: Matrix):
    orth = basis.gram_schmidt()[0]
    ans = t
    for i in reversed(range(basis.nrows())):
        y = orth[i]
        ans -= nearest(ans *y / y.norm()^2) * basis[i]
    return t - ans
