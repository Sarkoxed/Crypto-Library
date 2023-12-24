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


def test1():
    p = 0xA15C4FB663A578D8B2496D3151A946119EE42695E18E13E90600192B1D0ABDBB6F787F90C8D102FF88E284DD4526F5F6B6C980BF88F1D0490714B67E8A2A2B77
    a = 0x5E009506FCC7EFF573BC960D88638FE25E76A9B6C7CAEEA072A27DCD1FA46ABB15B7B6210CF90CABA982893EE2779669BAC06E267013486B22FF3E24ABAE2D42
    b = 0x2CE7D1CA4493B0977F088F6D30D9241F8048FDEA112CC385B793BCE953998CAAE680864A7D3AA437EA3FFD1441CA3FB352B0B710BB3F053E980E503BE9A7FECE

    E = EllipticCurve(GF(p), [a, b])
    b_x = 0x7F0489E4EFE6905F039476DB54F9B6EAC654C780342169155344ABC5AC90167ADC6B8DABACEC643CBE420ABFFE9760CBC3E8A2B508D24779461C19B20E242A38
    b_y = 0xDD04134E747354E5B9618D8CB3F60E03A74A709D4956641B234DAA8A65D43DF34E18D00A59C070801178D198E8905EF670118C15B0906D3A00A662D3A2736BF

    g = E(
        (
            3034712809375537908102988750113382444008758539448972750581525810900634243392172703684905257490982543775233630011707375189041302436945106395617312498769005,
            4986645098582616415690074082237817624424333339074969364527548107042876175480894132576399611027847402879885574130125050842710052291870268101817275410204850,
        )
    )
    A = E(
        (
            4748198372895404866752111766626421927481971519483471383813044005699388317650395315193922226704604937454742608233124831870493636003725200307683939875286865,
            2421873309002279841021791369884483308051497215798017509805302041102468310636822060707350789776065212606890489706597369526562336256272258544226688832663757,
        )
    )

    n1 = SmartAttack(g, A, p, prec=2)
    assert g * n1 == A


def test2():
    p = 54283205379427155782089046839411711
    a, b = (49850651047495986645822557378918223, 21049438014429831351540675253466229)
    E = EllipticCurve(GF(p), [a, b])
    G = E.lift_x(ZZ(1))
    A = E.lift_x(ZZ(1337))
    k = SmartAttack(G, A, p, 2)
    assert G * k == A


if __name__ == "__main__":
    test1()
    test2()
