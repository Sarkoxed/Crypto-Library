rotl = lambda x, k: ((x << k) | (x >> (64 - k))) & (2**64 - 1)
rotr = lambda x, k: rotl(x, 64 - k)

state = [0, 0, 0, 0]


def next(state):
    res = rotl((state[0] + state[3]) % 2**64, 23) + state[0]
    res %= 2**64

    t = (state[1] << 17) % 2**64

    state[2] ^= state[0]
    state[3] ^= state[1]
    state[1] ^= state[2]
    state[0] ^= state[3]

    state[2] ^= t

    state[3] = rotl(state[3], 45)

    return res


def test():
    state = [1, 2, 3, 4]
    exp = [
        41943041,
        58720359,
        3588806011781223,
        3591011842654386,
        9228616714210784205,
        9973669472204895162,
        14011001112246962877,
        12406186145184390807,
        15849039046786891736,
        10450023813501588000,
    ]
    res = [next(state) for _ in range(10)]
    assert res == exp


if __name__ == "__main__":
    test()
