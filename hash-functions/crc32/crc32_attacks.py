from sage.all import Matrix, vector, GF, PolynomialRing, ZZ, identity_matrix
from string import printable
import itertools as it
from crc32 import CRC32
from tqdm import tqdm


def to_vec(x: int, nbit: int = 32):
    res = ZZ(x).digits(2)
    res += [0] * (nbit - len(res))
    return vector(GF(2), res[::-1])


def to_int(v):
    return ZZ(list(v.change_ring(ZZ))[::-1], 2)


def get_lin_op():
    i_poly = 0xEDB88320 * 2 + 1
    mod = list(to_vec(i_poly, 33))
    F = GF(2**32, "x", modulus=mod)
    x = F([0, 1])

    M = Matrix(GF(2), 32, 32)
    for i in range(32):
        M.set_block(0, i, Matrix(list(x ** (8 + i))).T)
    return M


def shr(n):
    M = Matrix(GF(2), 32)
    M.set_block(n, 0, identity_matrix(32 - n))
    return M


def extract(n):
    M = Matrix(GF(2), 32)
    M.set_block(32 - n, 32 - n, identity_matrix(n))
    return M


def linearized_crc32(msg):
    L = get_lin_op()

    # N = len(msg)
    # c0 = to_vec(2**32 - 1)
    # c = L**N * c0 + c0
    # for i, u in enumerate(msg):
    #    c += L**(N - i) * to_vec(u)

    c = to_vec(2**32 - 1)
    for u in msg:
        c = L * (c + to_vec(u))
    c += to_vec(2**32 - 1)

    return to_int(c)


def algebraized_crc32(msg):
    i_poly = 0xEDB88320 * 2 + 1
    mod = list(to_vec(i_poly, 33))
    F = GF(2**32, "x", modulus=mod)
    x = F([0, 1])

    c = F(list(to_vec(2**32 - 1)))
    for m in msg:
        u = F(list(to_vec(m)))
        c = (c + u) * x**8
    c += F(list(to_vec(2**32 - 1)))
    return to_int(vector(list(c)))


def preimage(c, N):
    L = get_lin_op()
    right = L**-1 * (to_vec(c) - to_vec(2**32 - 1) - L**N * to_vec(2**32 - 1))

    left = Matrix(32, N * 8)
    for i in range(N):
        curidx = (N - i - 1) * 8
        curL = L ** (N - i - 1)
        curL = curL.T[-8:].T  # last 8 columns
        left.set_block(0, curidx, curL)

    sol = left.solve_right(right)
    if N <= 4:
        assert left.rank() == N * 8
    else:
        K = left.right_kernel().random_element()
        sol += K
    return bytes(to_int(sol[i : i + 8]) for i in range(0, 8 * N, 8))[::-1]


def printable_preimage(c, N, m=None, alph=printable):
    L = get_lin_op()
    S = shr(8)
    E = extract(8)
    T = L * E + S

    if m is None:
        m = N // 2

    base = {}
    hasher = CRC32()
    for word in tqdm(it.product(alph, repeat=m), total=len(alph) ** m):
        s = "".join(word)
        base[hasher.digest(s.encode()) ^ 0xFFFFFFFF] = s

    def imul(x, y):
        poly = 0xEDB88320
        res = 0
        while y:
            if y & 0x80000000:
                res ^= x
            if x & 1:
                x = poly ^ (x >> 1)
            else:
                x >>= 1
            y = (y << 1) % 2**32
        return res

    i_poly = 0xEDB88320 * 2 + 1
    mod = list(to_vec(i_poly, 33))
    F = GF(2**32, "x", modulus=mod)
    x = F([0, 1])
    mul = x**-8
    mul = to_int(vector(list(mul)))
    end = c ^ 0xFFFFFFFF

    for word in tqdm(
        it.product(alph.encode(), repeat=N - m), total=len(alph) ** (N - m)
    ):
        c = end
        for m in word:
            c = imul(c, mul) ^ m
        if c in base:
            return base[c].encode() + bytes(word)[::-1]


m = b"abobaabobga"
hasher = CRC32()
c = hasher.digest(m)
res = printable_preimage(c, len(m), 3)

print(f"CRC32({m}) = ".ljust(40) + f"{c}")
print(f"CRC32({res}) = ".ljust(40) + f"{hasher.digest(res)}")
