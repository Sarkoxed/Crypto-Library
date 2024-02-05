from py_ecc.bn128 import curve_order as q, G1, G2, multiply
from random import randint
import pickle


def gen_srs(N_points):
    tau = randint(1, q - 1)
    G1s = [G1]
    G2s = [G2]

    for _ in range(N_points - 1):
        G1s.append(multiply(G1s[-1], tau))
        G2s.append(multiply(G2s[-1], tau))
    return G1s, G2s


srs = gen_srs(20)
#with open("srs_data", "wb") as f:
#    pickle.dump(srs, f)
