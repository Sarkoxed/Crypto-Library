def closest_vertex(B, v):
    ans = B.change_ring(QQ).solve_right(v.change_ring(QQ))
    ans = [round(x) for x in ans]
    return ans
