def HenselLift(P, p, prec):
    E = P.curve()
    Eq = E.change_ring(QQ)
    Ep = Eq.change_ring(Qp(p, prec))
    x_P, y_P = P.xy()
    x_lift = ZZ(x_P)
    y_lift = ZZ(y_P)
    x, t, a1, a2, a3, a4, a6 =  var('x,y,a1,a2,a3,a4,a6')
    f(a1,a2,a3,a4,a6,x,y) = y**2 + a1*x*y + a3 * y - x**3 - a2*x**2 - a4 * x - a6
    g(y) = f(ZZ(Eq.a1()), ZZ(Eq.a2()), ZZ(Eq.a3()), ZZ(Eq.a4()), ZZ(Eq.a6()), ZZ(x_P), y)
    gDiff = g.diff()
    for i in range(1, prec):
        uInv = ZZ(gDiff(y=y_lift))
        u = uInv.inverse_mod(p**i)
        y_lift = y_lift - u * g(y_lift)
        y_lift = ZZ(Mod(y_lift, p**(i+1)))
        
    y_lift = y_lift + O(p**(i+1))
    return Ep([x_lift, y_lift])

def SmartAttack(P, Q, p, prec):
    E = P.curve()
    Eqq = E.change_ring(QQ)
    Eqp = Eqq.change_ring(Qp(p, prec))
    print(Eqp)

    P_Qp = HenselLift(P, p, prec)
    Q_Qp = HenselLift(Q, p, prec)

    p_times_P = p * P_Qp
    p_times_Q = p * Q_Qp

    x_P, y_P = p_times_P.xy()
    x_Q, y_Q = p_times_Q.xy()

    phi_P = -(x_P/y_P)
    phi_Q = -(x_Q/y_Q)

    k = phi_Q/phi_P
    k = Mod(k, p)
    return k

p = 0xa15c4fb663a578d8b2496d3151a946119ee42695e18e13e90600192b1d0abdbb6f787f90c8d102ff88e284dd4526f5f6b6c980bf88f1d0490714b67e8a2a2b77
a = 0x5e009506fcc7eff573bc960d88638fe25e76a9b6c7caeea072a27dcd1fa46abb15b7b6210cf90caba982893ee2779669bac06e267013486b22ff3e24abae2d42
b = 0x2ce7d1ca4493b0977f088f6d30d9241f8048fdea112cc385b793bce953998caae680864a7d3aa437ea3ffd1441ca3fb352b0b710bb3f053e980e503be9a7fece

E = EllipticCurve(GF(p), [a,b])
b_x = 0x7f0489e4efe6905f039476db54f9b6eac654c780342169155344abc5ac90167adc6b8dabacec643cbe420abffe9760cbc3e8a2b508d24779461c19b20e242a38
b_y = 0xdd04134e747354e5b9618d8cb3f60e03a74a709d4956641b234daa8a65d43df34e18d00a59c070801178d198e8905ef670118c15b0906d3a00a662d3a2736bf
 
g = (3034712809375537908102988750113382444008758539448972750581525810900634243392172703684905257490982543775233630011707375189041302436945106395617312498769005 , 4986645098582616415690074082237817624424333339074969364527548107042876175480894132576399611027847402879885574130125050842710052291870268101817275410204850)
A = (4748198372895404866752111766626421927481971519483471383813044005699388317650395315193922226704604937454742608233124831870493636003725200307683939875286865 , 2421873309002279841021791369884483308051497215798017509805302041102468310636822060707350789776065212606890489706597369526562336256272258544226688832663757)
d = {'iv': '719700b2470525781cc844db1febd994', 'encrypted_flag': '335470f413c225b705db2e930b9d460d3947b3836059fb890b044e46cbb343f0'}

A = E(A)
G = E(g)
k = SmartAttack(A, G, p, 100)
print(k)
assert G * k == A
