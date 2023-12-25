from sage.all import Zmod, gcd, EllipticCurve
import re


def ec_factor(n: int, m: int, Bound: int):
    G = Zmod(n)
    for _ in range(m):
        print(f"Curve: {_}")
        A = G.random_element()
        a, b = G.random_element(), G.random_element()
        B = b**2 - a**3 - A * a
        while (4 * A**3 + 27 * B**2) == 0:
            a, b = randint(1, n), randint(1, n)
            B = int((b**2 - a**3 - A * a) % n)

        try:
            E = EllipticCurve(G, [A, B])
        except ArithmeticError:
            return gcd(int(4 * A**3 + 27 * B**2), n)

        P = E((a, b))
        for i in range(1, Bound):
            if i % 10000 == 0:
                print(i)
            try:
                Q1 = i * P
                P = Q1
            except Exception as e:
                print(i)
                print(e)
                x = int(re.search(r"[0-9]+", str(e)).group(0))
                d = gcd(x, n)
                if d == n:
                    break
                else:
                    return d


if __name__ == "__main__":
    n = 580642391898843192929563856870897799650883152718761762932292482252152591279871421569162037190419036435041797739880389529593674485555792234900969402019055601781662044515999210032698275981631376651117318677368742867687180140048715627160641771118040372573575479330830092989800730105573700557717146251860588802509310534792310748898504394966263819959963273509119791037525504422606634640173277598774814099540555569257179715908642917355365791447508751401889724095964924513196281345665480688029639999472649549163147599540142367575413885729653166517595719991872223011969856259344396899748662101941230745601719730556631637
    k = ec_factor(n, m=100, Bound=10**5)
    print(k, n % k)
