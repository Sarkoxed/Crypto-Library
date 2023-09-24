from sage.all import *
from itertools import combinations

def group_lens(tups):
    d = dict()
    for sp in tups:
        r = d.setdefault(len(sp), [])
        d[len(sp)].append(sp)
    return d

def get_2packings(l):
    if len(l) == 0:
        return [[]]
    if len(l) == 1:
        return [[tuple(l)]]

    res = []
    f = l[0]
    for i in range(1, len(l)):
        other = get_2packings(l[1:i] + l[i + 1:])
        tmpres = [(f, l[i])]
        for x in other:
            res.append(tmpres + x)
    return res

def all_multiplications(d):
    if len(d) == 0:
        raise Exception("What")
    if len(d) == 1:
        return d[0]

    return [x * a for x in d[0] for a in all_multiplications(d[1:])]


def sqrt_sym_even(l_cycles, SG):
    if len(l_cycles) == 0:
        return [SG([])]

    packs2 = get_2packings(l_cycles) # getting all the possible [(X1, Y1), (X2, Y2), .., (Zn)] pairs.
    res = []
    for packing in packs2:
        res_cycle = SG([])

        tmp_pairs = []
        for pair in packing:
            tmpcycles = []
            second = list(pair[1])
            for shift in range(len(pair[0])): 
            # getting all tmpcycles such that tmpcycle^2 = pair for (i1, i2, i3, .., ik)(j1, j2, .., jk) it would be (i1, j1, i2, j2, ..., ik, jk), (i1, j2, i2, j3, ..., ik, j1) and all the shifts of (j)
                tmpcycle = []
                for x, y in zip(pair[0], second[shift:] + second[:shift]):
                    tmpcycle += [x, y]
                tmpcycles.append(SG(tuple(tmpcycle)))

            tmp_pairs.append(tmpcycles)
        
        tmp_res = all_multiplications(tmp_pairs)

        assert all(pow(x, 2) == SG(l_cycles) for x in tmp_res)
        res += tmp_res
    return res


def sqrt_sym_odd(l_cycles, SG):
    res = []
    for x in range(0, len(l_cycles) + 1, 2):  # need to check all the cases like for 5: (1, 1, 1, 1, 1), (2, 1, 1, 1), (2, 2, 1)
        for cycle2 in combinations(l_cycles, r=x):
            l_power1 = [x for x in l_cycles if x not in cycle2]
            power1_sqrt = SG([])
            for pow1 in l_power1:
                t = SG(pow1)
                power1_sqrt *= pow(t, pow(2, -1, t.order()))
            
            even_cycles = sqrt_sym_even(cycle2, SG)
            cycles = [x * power1_sqrt for x in even_cycles]
            assert all(x**2 == SG(l_cycles) for x in cycles)
            res += cycles
    return res
       

def sqrt_sym(p, SG):
    tups = p.cycle_tuples(singletons=True)
    groups = group_lens(tups)

    possibilities = []
    
    for l, l_cycles in groups.items():
        if l % 2 == 1:
            tmp = sqrt_sym_odd(l_cycles, SG)
        else:
            tmp = sqrt_sym_even(l_cycles, SG)
        #print(l_cycles)
        #print(tmp)
        possibilities.append(tmp)
        #print()
        #print()
    res = all_multiplications(possibilities)
    return res


if __name__ == "__main__":
    S = SymmetricGroup(10)
    for _ in range(20):
        print(f"Round {_}")

        s = S.random_element()
        print("s = ", s)
        v = s**2
        print("s^2 = ", v)
        res = sqrt_sym(v, S)
        real_res = [x for x in S if x**2 == v]
        assert len(res) == len(real_res)
        assert set(res) == set(real_res)

