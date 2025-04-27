from sage.all import (
    QQ,
    Matrix,
    PolynomialRing,
    identity_matrix,
    sin,
    taylor,
    var,
    vector,
)

x = var("x")
P = PolynomialRing(QQ, x)


def compute_pade(f, N, M):
    t_cfs = taylor(f, x, 0, N + M).list()
    if len(t_cfs) != N + M + 1:
        t_cfs.extend([0] * (N + M + 1 - len(t_cfs)))

    C = Matrix(QQ, N + M + 1)
    C.set_block(0, 0, -identity_matrix(N + 1))

    for i in range(N + M + 1):
        C.set_block(i, N + 1, Matrix(t_cfs[:i][::-1][:M]))

    print(C)
    print(-vector(t_cfs))
    res_cfs = list(C.solve_right(-vector(t_cfs)))

    A = P(res_cfs[: N + 1])
    B = P([1] + res_cfs[N + 1 :])
    return A / B


if __name__ == "__main__":
    print(compute_pade(sin(x), 3, 3))
    print(compute_pade(1 + 2 * x + 3 * x**2 + 4 * x**3 + 5 * x**4, 2, 2))
