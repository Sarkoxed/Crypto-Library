rotl = lambda x, k: ((x << k) | (x >> (32 - k))) & (2**32 - 1)
rotr = lambda x, k: rotl(x, 32 - k)

state = [0, 0, 0, 0]


def next(state):
    res = rotl((state[0] + state[3]) % 2**32, 7) + state[0]
    res %= 2**32

    t = (state[1] << 9) % 2**32

    state[2] ^= state[0]
    state[3] ^= state[1]
    state[1] ^= state[2]
    state[0] ^= state[3]

    state[2] ^= t

    state[3] = rotl(state[3], 11)

    return res


def test():
    state = [1, 2, 3, 4]
    exp = [
        641,
        1573767,
        3222811527,
        3517856514,
        836907274,
        4247214768,
        3867114732,
        1355841295,
        495546011,
        621204420,
    ]
    res = [next(state) for _ in range(10)]
    assert res == exp


if __name__ == "__main__":
    test()
