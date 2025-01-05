import pytest
from montgomery import AffineMontgomeryPoint, Montgomery, ProjectiveMontgomeryPoint
from Crypto.Util.number import getPrime, getRandomNBitInteger

@pytest.mark.parametrize('nbit', [256])
def test_random_curve(nbit):
    p = getPrime(nbit)
    A = getRandomNBitInteger(nbit)
    B = getRandomNBitInteger(nbit)

    if B % p == 0 or pow(A, 2, p) == 4:
        return
    
    E_M = Montgomery(A, B, p)
    
    P_M = E_M.random_point()
    P_W = E_M.to_weierstrass(P_M)

    m = getRandomNBitInteger(nbit)
    Q_M = m * P_M
    Q_W = m * P_W

    assert Q_W == E_M.to_weierstrass(Q_M)

@pytest.mark.parametrize('nbit', [256])
def test_kernel(nbit):
    p = getPrime(nbit)
    A = getRandomNBitInteger(nbit)
    B = getRandomNBitInteger(nbit)

    if B % p == 0 or pow(A, 2, p) == 4:
        return
    
    E = Montgomery(A, B, p)
    P = E.random_point()

    order = P.order_lame()
    m = getRandomNBitInteger(nbit)

    P_ = ProjectiveMontgomeryPoint.from_affine(P)

    Q1 = ProjectiveMontgomeryPoint.scalarmul(P_, m % order)
    Q2 = ProjectiveMontgomeryPoint.scalarmul(P_, -m % order)
    assert Q1 == Q2
    
@pytest.mark.parametrize('execution_number', range(100))
def test_scalar(execution_number):
    E = Montgomery(-1, 1, 2651020721)
    m = 1234356457

    P = E.random_point()
    tm = m * P

    P1 = ProjectiveMontgomeryPoint.from_affine(P)
    t_m = ProjectiveMontgomeryPoint.scalarmul(P1, m)
    t_m.normalize()
    
    assert tm.x == t_m.x

@pytest.mark.parametrize('execution_number', range(100))
def test_recovery(execution_number):
    E = Montgomery(-1, 1, 2651020721)
    m = 1234356457

    P = E.random_point()
    tm = m * P

    P1 = ProjectiveMontgomeryPoint.from_affine(P)
    t_m, t_m_1 = ProjectiveMontgomeryPoint.scalarmul(P1, m, recovery=True)

    tm1 = ProjectiveMontgomeryPoint.recover(P, t_m, t_m_1)
    assert tm == tm1

@pytest.mark.parametrize('execution_number', range(100))
def test_uniform_scalar(execution_number):
    E = Montgomery(-1, 1, 2651020721)
    m = 1234356457

    P = E.random_point()
    tm = m * P

    P1 = ProjectiveMontgomeryPoint.from_affine(P)
    t_m = ProjectiveMontgomeryPoint.uniform_ladder(P1, m)
    t_m.normalize()
    
    assert tm.x == t_m.x

@pytest.mark.parametrize('execution_number', range(100))
def test_euclid2d(execution_number):
    E = Montgomery(-1, 1, 2651020721)
    m = getRandomNBitInteger(32)
    n = getRandomNBitInteger(32)

    P = E.random_point()
    Q = E.random_point()
    R = m * P + n * Q

    P1 = ProjectiveMontgomeryPoint.from_affine(P)
    Q1 = ProjectiveMontgomeryPoint.from_affine(Q)
    P_Q1 = ProjectiveMontgomeryPoint.from_affine(P - Q)

    R1 = ProjectiveMontgomeryPoint.EUCLID2D(P1, Q1, P_Q1, m, n)
    R1.normalize()

    assert R.x == R1.x

@pytest.mark.parametrize('execution_number', range(100))
def test_euclidian_pseudoscalar(execution_number):
    E = Montgomery(-1, 1, 2651020721)
    m = getRandomNBitInteger(32)

    P = E.random_point()
    R = m * P

    P1 = ProjectiveMontgomeryPoint.from_affine(P)
    R1 = ProjectiveMontgomeryPoint.euclidian_pseudoscalar(P1, m)
    R1.normalize()

    assert R.x == R1.x
