from z3 import *

l = [BitVec(f"s_{i}", 40) for i in range(1, 112)]

five = And([And(x <= 500, x > 0) for x in l])

res = []
for j in range(len(l)):
    x = l[j]
    c = l[:j] + l[j + 1 :]
    res.append(x % 10 == sum(c) % 10)
res = And(res)

print(solve(And(sum(l) == 500, And(five), res)))
