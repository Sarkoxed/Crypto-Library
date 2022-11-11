from Crypto.Util.number import GCD


def f(x: int, N: int):
    return (pow(x, 2, N) + 1) % N


def pollard_rho(N: int, f=f):
    x = y = 0
    while GCD(abs(x - y), N) == 1 or GCD(abs(x - y), N) == N:
        x = f(x, N)
        y = f(f(y, N), N)
    return GCD(abs(x - y), N)


N = int(input())
print(pollard_rho(N))
