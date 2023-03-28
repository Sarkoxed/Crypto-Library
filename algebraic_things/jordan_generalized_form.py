from sage.all import *

def get_jordan_ordinary(A, lam, s): # https://math.stackexchange.com/questions/2441810/jordan-form-number-of-blocks
    n = A.dimensions()[0]
    R = A.base_ring()
    # number_of_blocks = n - (A - lam * identity_matrix(R, n)).rank()
    bks = []
    for k in range(1, s + 2):
        dk = kernel((A - lam * identity_matrix(R, n))**k).dimension()
        dk1 = kernel((A - lam * identity_matrix(R, n))**(k - 1)).dimension()
        bk = dk - dk1
        bks.append(bk)

    # print(bks)
    blocks = dict()
    for i in range(len(bks) - 1):
        blocks[i+1] = bks[i] - bks[i+1]

    # print(blocks)
    jor = zero_matrix(R, s)
    pos = 0
    jordan_blocks = []
    for size, number in blocks.items():
        block = jordan_block(lam, size)
        for k in range(number):
            if block not in jordan_blocks:
                jordan_blocks.append(block)
            jor.set_block(pos, pos, block)
            pos += size
    return jor.change_ring(R), jordan_blocks


def gen_jordan_general(A):
    n = A.dimensions()[0]
    R = A.base_ring()

    f = list(factor(A.charpoly()))
    jor = zero_matrix(R, n)
    pos = 0
    blocks = []
    for g, s in f:
        print(g.is_primitive())
        d = g.degree()
        if d == 1:  # based jordan form
            block, prim_blocks = get_jordan_ordinary(A, g.roots()[0][0], s)
            #for b in prim_blocks:
            #    blocks.append((b, block, s, True)) # i do not know how to process it and i want to sleep
            blocks.append((block, block, s, True))
        else:
            block = zero_matrix(R, d * s)
            gi = companion_matrix(g).T
            W = zero_matrix(R, d)
            W[d - 1, 0] = 1
            for i in range(s - 1):
                block.set_block(i * d, i * d, gi)
                block.set_block(i * d, (i +1)* d, W)

            block.set_block(d * (s - 1), d * (s - 1), gi)
            blocks.append((gi, block, s, False)) # TODO: in paper p^r >= d * s, but it's not working(obviously ther's a mistake in paper). See line 35

        jor.set_block(pos, pos, block)
        pos += d * s
    return jor, blocks


def get_matrix_order(A, p):  # https://arxiv.org/pdf/1505.00776.pdf
    J, blocks = gen_jordan_general(A)
    assert J.multiplicative_order() == A.multiplicative_order()

    supposed_res = [bl.multiplicative_order() for _, bl, _, _ in blocks]
    got_res = []


    ords = []
    rs = []
    for g, bl, s, flag in blocks:
        m = g.multiplicative_order()  # if corresponding polynomial is primitive and irreducible => p^(deg(f)) - 1
        r = 0
        bl = pow(bl, m) - identity_matrix(A.base_ring(), bl.dimensions()[0])
        if s >= 2 and not flag:
            while not bl.is_zero():
                bl = pow(bl, p)      # maybe something smarter can be done
                r += 1
        got_res.append(pow(p, r) * m)
        rs.append(r)
        ords.append(m)

    #print(supposed_res, lcm(supposed_res))
    #print(got_res, lcm(got_res))
    #assert gcd(pow(p, max(rs)), lcm(ords)) == 1
    #res = pow(p, max(rs)) * lcm(ords) # doesn't work becaues I skip the jordan cell for x + 1
    res = lcm([pow(p, max(rs))] + ords)
    return res

# TODO: I guess that this paper has a way more mistakes and that this jordan form has it's own funnies when s >= 2
# YES IT FAILS WHEN THE POLYNOMIAL IS NOT PRIMITIVE AND THE POWER IS >= 2

if __name__ == "__main__":
    for i in range(100):
        p = 2 #random_prime(100)
        n = randint(2, 20)
        while True:
            M = MatrixSpace(GF(p), n).random_element()
            if det(M) > 0:
                break
        M = Matrix(GF(p), M)
        #print(p, n, list(M), sep = ", ")
        print(factor(M.charpoly()))
        ord1 = M.multiplicative_order()
        ord2 = get_matrix_order(M, p)
        #print(ord1, ord2, ord2 / gcd(ord1, ord2),"orders")
        assert ord1 == ord2
        print("--" * 50)
