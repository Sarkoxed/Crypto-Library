from small_rng import rng_u64, from_u64, rng_u32, rng_range

def test_small_rng_u64():
    state = 1709415319
    seed = from_u64(state)

    rng = rng_u64(seed)
    assert [rng.__next__() for _ in range(2)] == [13798785537587295438, 5373385370510764734]

def test_small_rng_u32():
    state = 1709415498
    seed = from_u64(state)

    rng = rng_u32(seed)
    assert [rng.__next__() for _ in range(2)] == [3758079556, 2134447775]

def test_small_rng_range():
    state = 1709416203
    seed = from_u64(state)

    rng = rng_range(seed, 1, 100)
    assert [rng.__next__() for _ in range(2)] == [71, 2]
