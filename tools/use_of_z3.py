import z3


def rua(n):
    Q = [z3.BitVec("Q_{}".format(i), 42) for i in range(n)]
    val_c = [z3.And(1 <= Q[i], Q[i] <= n) for i in range(n)]
    col_c = [z3.Distinct(Q)]
    con_c = [sum(Q[i] * ((-2) ** i) for i in range(n)) == 0]
    solver = z3.Solver()
    solver.add(val_c + col_c + con_c)

    result = ""
    if n % 3 == 1:
        return b"TINP"
    elif solver.check() == z3.sat:
        m = solver.model()
        print("{}:".format(n), end=" ")
        for i in Q:
            result += str(m[i])
            result += ","
        return result.encode()[:-1]  # 去掉最后一个逗号
    else:
        return b"???"


print(rua(101))
