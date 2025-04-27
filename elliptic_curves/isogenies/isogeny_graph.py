import itertools
import itertools as it

import matplotlib.pyplot as plt
import networkx as nx
from sage.all import (
    GF,
    EllipticCurve,
    EllipticCurve_from_j,
    classical_modular_polynomial,
)

from isogenies import get_all_isogenous_curves


def brute_graph(p, l=3):
    G = nx.MultiGraph()
    # G = nx.Graph()

    used = {}
    js = {}

    for j in range(p):
        Ej = GF(p)(j)
        E = EllipticCurve_from_j(Ej)

        if Ej not in js:
            js[Ej] = f"j{len(js)}"

        G.add_node(js[Ej])
        for neigh_j, m in get_all_isogenous_curves(E, l):
            if (Ej, neigh_j) in used:
                #        print(Ej, neigh_j, used[(Ej, neigh_j)], m)
                #        assert used[(Ej, neigh_j)] == m
                continue
            if neigh_j not in js:
                js[neigh_j] = f"j{len(js)}"

            used[(Ej, neigh_j)] = m
            used[(neigh_j, Ej)] = m
            for _ in range(m):
                G.add_edge(js[Ej], js[neigh_j])

    return G


def successive_graph(E, l=3, bound=4):
    G = nx.MultiGraph()
    # G = nx.Graph()

    used = {}
    depth = 0
    js = {}
    stack = [E.j_invariant()]
    while len(stack) != 0:
        print(len(stack), depth, bound)
        Ej = stack.pop()
        if Ej in used:
            continue

        used[Ej] = 0
        if Ej not in js:
            js[Ej] = f"j{len(js)}"
        G.add_node(js[Ej])
        depth += 1

        E = EllipticCurve_from_j(Ej)

        for neigh_j, m in get_all_isogenous_curves(E, l):
            if depth < bound:
                stack.append(neigh_j)

            if (Ej, neigh_j) in used:
                assert used[(Ej, neigh_j)] == m
                continue
            used[(Ej, neigh_j)] = m
            used[(neigh_j, Ej)] = m
            if neigh_j not in js:
                js[neigh_j] = f"j{len(js)}"

            for _ in range(m):
                G.add_edge(js[Ej], js[neigh_j])
    return G


# G = brute_graph(11, 3)
# G = successive_graph(EllipticCurve_from_j(GF(11)(2)), 3)
G = successive_graph(EllipticCurve(GF(97**2), [1, 22]), 3, bound=10)


# pos = nx.shell_layout(G)
# pos = nx.planar_layout(G)
pos = nx.spring_layout(G)
connectionstyle = [f"arc3,rad={r}" for r in it.accumulate([0.15] * 4)]

nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_labels(G, pos, font_size=10)
nx.draw_networkx_edges(G, pos, connectionstyle=connectionstyle)

# plt.show()
plt.savefig("isogeny_graphs/supersingular_97_3.png")
