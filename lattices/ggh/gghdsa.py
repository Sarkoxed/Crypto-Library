from ggh import *


def get_signature(pub, priv, d):
    v = Babai_algorithm(priv, d)
    s = Matrix(pub).solve_left(v)
    return s


def verify_signature(pub, d, s):
    s1 = sum([i * j for i, j in zip(s, pub)])
    print(f"Svec: {s1}")
    print(f"dist: {(d - s1).norm().n()}")
    v = Babai_algorithm(pub, d)
    s1 = sum([i * j for i, j in zip(v, pub)])
    print(f"dist bad: {(d - s1).norm().n()}")


if __name__ == "__main__":
    dim = int(input("dim: "))
    print("Pub")
    pub = [vector([int(input()) for i in range(dim)]) for i in range(dim)]
    #    print("Priv")
    #    priv = [vector([int(input()) for i in range(dim)]) for i in range(dim)]
    print("D:")
    d = vector([int(input()) for i in range(dim)])
    #    s = get_signature(pub, priv, d)
    s = vector([int(input()) for i in range(dim)])
    print(s)
    verify_signature(pub, d, s)
