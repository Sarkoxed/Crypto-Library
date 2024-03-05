from xoshiro256plusplus import next as next_xosh, rotr
from xoshiro128plusplus import rotr as rotr32
import struct

def pcg32(state):
    mul = 6364136223846793005
    inc = 11634580027462260723

    state = (state * mul + inc) % 2**64

    xorshifted = (((state >> 18) ^ state) >> 27) % 2**32
    rot = state >> 59

    x = rotr32(xorshifted, rot)
    return struct.pack("<I", x), state


def from_u64(state) -> list[int]:
    buf = b''
    for i in range(8):
        out, state = pcg32(state)
        buf += out

    # into_remainder part that I didn't get
    return buf

def rng_u64(seed):
    if all(x == 0 for x in seed):
        seed = from_u64(0)

    state = list(struct.unpack("<4Q", seed))
    while True:
        yield next_xosh(state)

def rng_u32(seed):
    if all(x == 0 for x in seed):
        seed = from_u64(0)

    state = list(struct.unpack("<4Q", seed))
    
    while True:
        yield next_xosh(state) >> 32

def rng_range(seed, a, b):
    if all(x == 0 for x in seed):
        seed = from_u64(0)

    state = list(struct.unpack("<4Q", seed))

    range = b - a
    while True:
        if range == 0:
            yield next_xosh(state) >> 32
        else:
            # rust stuff that we probably won't encounter... I was wrong
            zone = ((range << (32 - range.bit_length())) - 1) % 2**32
            while True:
                v = next_xosh(state) >> 32
                res, rem = divmod(range * v, 2**32)
                if rem <= zone:
                    break
#            res, rem = divmod(range * v, 2**32)
            yield a + res


if __name__ == "__main__":
#    state = int(input("state: "))
    state = 1709426252
    for i in range(-5, -5 + 11):
        seed = from_u64(state + i)
        rng = rng_range(seed, 1, 101).__next__()
        print(rng, end = ', ')
