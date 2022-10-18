#  K - base field, P = K[Y] - ring of univariate polynomials over K, P[Y] - ring of univariate polynomials over P

# input:
# base field K
# nonnegative intgers d, n, k, t
# F from P[Y] monic of degree d with coefficients of degree < n
# M from P of degree n

# output : all p from P such that
#               - deg(gcd(F(p), M)) >= t
#               - deg(p) <= k
