#!/usr/bin/python

import gmpy2
import math
import os
import sys

_DEBUG = True

SEED = gmpy2.mpz(os.urandom(32).hex(), 16)
STATE = gmpy2.random_state(SEED)


def get_prime(state, bits):
    return gmpy2.next_prime(gmpy2.mpz_urandomb(state, bits) | (1 << (bits - 1)))


def get_smooth_prime(state, bits, smoothness=16):
    p = gmpy2.mpz(2)
    p_factors = [p]
    while p.bit_length() < bits - 2 * smoothness:
        factor = get_prime(state, smoothness)
        p_factors.append(factor)
        p *= factor

    bitcnt = (bits - p.bit_length()) // 2

    while True:
        prime1 = get_prime(state, bitcnt)
        prime2 = get_prime(state, bitcnt)
        tmpp = p * prime1 * prime2
        if tmpp.bit_length() < bits:
            bitcnt += 1
            continue
        if tmpp.bit_length() > bits:
            bitcnt -= 1
            continue
        if gmpy2.is_prime(tmpp + 1):
            p_factors.append(prime1)
            p_factors.append(prime2)
            p = tmpp + 1
            break

    p_factors.sort()

    return (p, p_factors)


e = 0x10001

if __name__ == "__main__":
    while True:
        p, p_factors = get_smooth_prime(STATE, 1024, 16)
        if len(p_factors) != len(set(p_factors)):
            continue

        q, q_factors = get_smooth_prime(STATE, 1024, 30)
        if len(q_factors) != len(set(q_factors)):
            continue
        factors = p_factors + q_factors

        if e not in factors:
            break
