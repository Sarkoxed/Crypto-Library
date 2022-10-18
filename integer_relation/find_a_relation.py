# suppose we are given a vector of real numbers (a1, ..., an) and let (a1', ..., an') vector of their rational approximations
# let's consider lattice spanned by the (n+1) dimensional vectors v^(i) where vj^(i) = delta(i, j) for 1 <=i,j<=n
# and v(n+1)^(i) = C * ai'. C - large rational constant
# if w - short vector in reduced basis for L
# w = (w1, ....., wn, C * Sum(wi * ai'))
# 
# then abs(sum(wi * ai')) is small and thus (w1, ..., wn) is a good candidate for an integer relation for the vector(a1, ..., an). With increasing C we improve our chances of correctly determining which vectors in the reduced basis correspond to an integer relation for (a1, ..., an) and which do not.
# sometimes we are looking for integers, such that (sum(wi * ai)) is non-zero byt small in absolute value.

# for examle de Weger uses an LLL-type alog to look for distinct integers x, y such that x and y are composed exclusively from the given set of primes, say: {p1, ..., ps}, and abs(x-y) is small
# then x/y = p1**e1 * ... * ps**es is close to 1(with e1,..., es in Z) and therefore e1 * log(p1) + ... + es * log(ps) ~ 0




from sage.all import *
