from sage.all import GF, QQ, ZZ, EllipticCurve, Mod, O, Qp, var


def HenselLift(P, p, prec):
    E = P.curve()
    Eq = E.change_ring(QQ)
    Ep = Eq.change_ring(Qp(p, prec))
    x_P, y_P = P.xy()
    x_lift = ZZ(x_P)
    y_lift = ZZ(y_P)

    x, y, a1, a2, a3, a4, a6 = var("x,y,a1,a2,a3,a4,a6")
    f = y**2 + a1 * x * y + a3 * y - x**3 - a2 * x**2 - a4 * x - a6

    g = f(
        a1=ZZ(Eq.a1()),
        a2=ZZ(Eq.a2()),
        a3=ZZ(Eq.a3()),
        a4=ZZ(Eq.a4()),
        a6=ZZ(Eq.a6()),
        x=ZZ(x_P),
    )  # g(y)
    gDiff = g.diff()
    for i in range(1, prec):
        uInv = ZZ(gDiff(y=y_lift))
        u = uInv.inverse_mod(p**i)
        y_lift = y_lift - u * g(y=y_lift)
        y_lift = ZZ(Mod(y_lift, p ** (i + 1)))

    y_lift = y_lift + O(p ** (i + 1))
    return Ep((x_lift, y_lift))


def SmartAttack(P, Q, p, prec):
    E = P.curve()
    Eqq = E.change_ring(QQ)
    Eqp = Eqq.change_ring(Qp(p, prec))

    P_Qp = HenselLift(P, p, prec)
    Q_Qp = HenselLift(Q, p, prec)

    p_times_P = p * P_Qp
    p_times_Q = p * Q_Qp

    x_P, y_P = p_times_P.xy()
    x_Q, y_Q = p_times_Q.xy()

    lambda_P = -(x_P / y_P)
    lambda_Q = -(x_Q / y_Q)

    k = lambda_Q / lambda_P
    k = Mod(k, p)
    return k
