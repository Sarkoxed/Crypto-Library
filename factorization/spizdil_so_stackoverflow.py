def is_fermat_probable_prime(n, *, trials = 32):
    # https://en.wikipedia.org/wiki/Fermat_primality_test
    import random
    if n <= 16:
        return n in (2, 3, 5, 7, 11, 13)
    for i in range(trials):
        if pow(random.randint(2, n - 2), n - 1, n) != 1:
            return False
    return True

def pollard_rho_factor(N, *, trials = 16):
    # https://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm
    import random, math
    for j in range(trials):
        i, stage, y, x = 0, 2, 1, random.randint(1, N - 2)
        while True:
            r = math.gcd(N, x - y)
            if r != 1:
                break
            if i == stage:
                y = x
                stage <<= 1
            x = (x * x + 1) % N
            i += 1
        if r != N:
            return [r, N // r]
    return [N] # Pollard-Rho failed

def trial_division_factor(n, *, limit = None):
    # https://en.wikipedia.org/wiki/Trial_division
    fs = []
    while n & 1 == 0:
        fs.append(2)
        n >>= 1
    d = 3
    while d * d <= n and limit is None or d <= limit:
        q, r = divmod(n, d)
        if r == 0:
            fs.append(d)
            n = q
        else:
            d += 2
    if n > 1:
        fs.append(n)
    return fs

def factor(n):
    if n <= 1:
        return []
    if is_fermat_probable_prime(n):
        return [n]
    fs = trial_division_factor(n, limit = 1 << 12)
    if len(fs) >= 2:
        return sorted(fs[:-1] + factor(fs[-1]))
    fs = pollard_rho_factor(n)
    if len(fs) >= 2:
        return sorted([e1 for e0 in fs for e1 in factor(e0)])
    return trial_division_factor(n)


print(factor(580642391898843192929563856870897799650883152718761762932292482252152591279871421569162037190419036435041797739880389529593674485555792234900969402019055601781662044515999210032698275981631376651117318677368742867687180140048715627160641771118040372573575479330830092989800730105573700557717146251860588802509310534792310748898504394966263819959963273509119791037525504422606634640173277598774814099540555569257179715908642917355365791447508751401889724095964924513196281345665480688029639999472649549163147599540142367575413885729653166517595719991872223011969856259344396899748662101941230745601719730556631637))
