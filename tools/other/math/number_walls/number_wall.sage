def get_number_wall_poly(init, n) -> list[list[int]]:
    # init - sequence, n - estimated depth
    first_row = [1 for i in range(len(init))]
    second_row = [x for x in init]
    ans = [first_row, second_row]
    for row in range(1, n + 1):
        print(row)
        tmp = [0 for i in range(row)]  # forming triangular base

        for j in range(row, len(init) - row):
            c, a, b, e = ans[row - 1][j], ans[row][j-1], \
                         ans[row][j+1], ans[row][j]
            # taking plus around [row][j]

            if c != 0:
                d = expand(factor((e**2 - a * b) / c))
#                print(d)
                tmp.append(d)
            else:
                print("Something wrong")
                exit(1)

        for k in range(len(tmp), len(init)):
            tmp.append(0)
        ans.append(tmp)
        if tmp == [0 for _ in range(len(init))]:
            return ans
    return ans


def get_number_wall(init, n) -> list[list[int]]:
    # init - sequence, n - estimated depth
    first_row = [1 for i in range(len(init))]
    second_row = [x for x in init]
    ans = [first_row, second_row]
    for row in range(1, n + 1):
        print(row)
        tmp = [0 for i in range(row)]  # forming triangular base

        for j in range(row, len(init) - row):
            c, a, b, e = ans[row - 1][j], ans[row][j-1], \
                         ans[row][j+1], ans[row][j]
            # taking plus around [row][j]

            if c != 0:
                d = (e**2 - a * b) / c
                tmp.append(d)
            else:
                print("Something wrong")
                exit(1)

        for k in range(len(tmp), len(init)):
            tmp.append(0)
        ans.append(tmp)
        if tmp == [0 for _ in range(len(init))]:
            return ans
    return ans



x = var('x')
#initial = [1, 1, 2, 3, 5, 8, 13, 21]
#initial = [1, 1, 1, 3, 5, 9, 17, 31, 57, 105, 193, 355, 653]
#initial = [112, 56, 84, 42, 204, 54][1:]
#from output import initial
#initial = [Integer(x) for x in initial]
#from output1 import initial
initial = [1, 3, 1, 5, 1, 2, 9]
res = get_number_wall(initial, len(initial))

#initial1 = [initial[i] - x * initial[i-1] for i in range(1, len(initial))]
#res1 = get_number_wall_poly(initial1, len(initial1))

#print(len(res), len(res1))
#
#print(res)
#print(res1)
print(Matrix(res))
#print(Matrix(res1))

#with open("res.py", "wt") as f:
#    f.write(f"out = {res}")

#with open("res1.py", "wt") as f:
#    f.write(f"out = {res1}")
